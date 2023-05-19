import hashlib
import os
import pathlib
import re
import shutil
import threading
import time
from contextlib import suppress

import yaml
from dotenv import dotenv_values
from invoke import Collection, Context, task

DOCKERFILE_DJANGO_DEV = "./conf_build/Dockerfile_Django_Dev"
DOCKERFILE_DJANGO_PROD = "./conf_build/Dockerfile_Django_Prod"
DOCKERFILE_DJANGO = "./Dockerfile_Django"
#
DOCKERFILE_VUE_DEV = "./conf_build/Dockerfile_Vue_Dev"
DOCKERFILE_VUE_BUILD = "./conf_build/Dockerfile_Vue_Build"
DOCKERFILE_VUE = "./Dockerfile_Vue"


FILE_DEV = [
    DOCKERFILE_DJANGO_DEV,
    DOCKERFILE_VUE_DEV,
]
FILE_PROD = [
    DOCKERFILE_DJANGO_PROD,
]
FILE_ALL = [
    *FILE_DEV,
    *FILE_PROD,
]
LIST_PROD_APP = " ".join(["app", "db", "nginx_vue", "nginx_static"])
LIST_TEST_DJANGO_APP = " ".join(["app", "db"])

# Скрыть из вывода в консоли задачи который skip
ANSIBLE_HIDE_SKIP = "export ANSIBLE_DISPLAY_SKIPPED_HOSTS=no &&"

######################
# Для диплой


@task
def publish(ctx, limit, build_vue=False):
    """Отправить проект на прод

    limit: Ограничить выполннение только для указных серверов, если указать `all`, то выполнится для всех
    """
    # Выполнить сборку VUE если это необходимо
    if build_vue:
        buildVueIfNotExist(ctx)
    # Выполнить диплой
    runAnsibleScript(ctx, limit, "publush.yml")


@task
def dump(ctx, limit):
    """Сделать дамб базы на проде, и копировать её на текущую машину
    в ./backend/fixtures/api.json

    limit: Ограничить выполннение только дял указных серверов, если указать `all`, то выполнится для всех
    """
    runAnsibleScript(ctx, limit, "dump_api.yml")


@task
def deletePgdata(ctx, limit):
    """Удаление папки pgdata из серверов

    Это может быть необходимо если внесены большие правки в БД
    И единственный способ исправить конфликт, это удалить БД

    limit: Ограничить выполннение только дял указных серверов, если указать `all`, то выполнится для всех
    """
    runAnsibleScript(ctx, limit, "delete_pgdata.yml")


@task
def testDjango(ctx, prod=False):
    """Выполнить тесты Django в контейнере"""
    print("Запуск 1::::::::::::;;")
    restart(ctx, prod=prod, detach=True, list_prod_app=LIST_TEST_DJANGO_APP)
    print("Запуск 2::::::::::::;;")
    # command = "pytest"
    # ctx.run(f"docker-compose exec app {command}", pty=True)


######################
# Взаимодействие с docker-compose


@task
def build(ctx, prod=False, list_prod_app: str = ""):
    """Собрать docker-compose"""
    ConfToRoot(ctx, prod)
    if not list_prod_app:
        list_prod_app = LIST_PROD_APP
    ctx.run(f"docker-compose build {list_prod_app}" if prod else "docker-compose build")
    RootToConf(ctx)


@task
def run(ctx, prod=False, detach=False, list_prod_app: str = ""):
    """Запустить docker-compose"""
    ConfToRoot(ctx, prod)
    build_html()
    if not list_prod_app:
        list_prod_app = LIST_PROD_APP
    ctx.run(
        f"docker-compose up {'-d' if detach else ''} {list_prod_app}"
        if prod
        else "docker-compose up"
    )
    RootToConf(ctx)


@task
def restart(ctx, prod=False, detach=False, list_prod_app: str = ""):
    print("prod: ", prod)
    """Перезапустить docker-compose"""
    down(ctx, prod)
    build(ctx, prod, list_prod_app)
    run(ctx, prod, detach, list_prod_app)


@task
def down(ctx, prod=False):
    """Остановить docker-compose"""
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose down")
    RootToConf(ctx)


@task
def logs(ctx, prod=False):
    """Посмотреть логи"""
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose logs")
    RootToConf(ctx)


######################
# Перенеиспользуемые задачи


@task
def ConfToRoot(ctx, prod=False):
    """Копировать конфигурационные файлы в корен проекта"""
    shutil.copyfile(
        DOCKERFILE_DJANGO_PROD if prod else DOCKERFILE_DJANGO_DEV,
        DOCKERFILE_DJANGO,
    )


@task
def RootToConf(ctx):
    """Отчистка конфигурационных файлов из кореня проекта"""
    with suppress(FileNotFoundError):
        os.remove(DOCKERFILE_DJANGO)


@task
def buildVueIfNotExist(ctx):
    """Скомпелировать VUE проект, если он был изменен"""

    def get_value_from_yaml(yaml_file, key):
        with open(yaml_file, "r") as file:
            yaml_data = yaml.safe_load(file)
            value = yaml_data.get(key)
        return value

    def insert_value_to_yaml(yaml_file, key, value):
        with open(yaml_file, "r") as file:
            yaml_data = yaml.safe_load(file)

        yaml_data[key] = value

        with open(yaml_file, "w") as file:
            yaml.safe_dump(yaml_data, file)

    # 1. Получить SHA265 у папки
    front_vue_hash_select = get_folder_sha256(pathlib.Path("front_vue"))
    # 2. Проверить конфигурацию проекта
    front_vue_hash = get_value_from_yaml("app_config.yml", "front_vue_hash")
    if front_vue_hash != front_vue_hash_select:
        front_vue_hash = front_vue_hash_select
        insert_value_to_yaml("app_config.yml", "front_vue_hash", front_vue_hash)
        # Сборка Vue.js приложения на локальной машине перед диплоем
        ctx.run(f"docker build -t dockerfile_vue_prod -f {DOCKERFILE_VUE_BUILD} .")
        ctx.run(
            "docker run -v ./front_vue:/app -v /app/node_modules dockerfile_vue_prod"
        )
        ctx.run("sudo chown $USER:$USER -R ./front_vue")


######################
# Утилиты


def build_html():
    """Изменение index.html указываем хост к Django серверу,
    в зависимости от сервера хост будет разный"""

    env_dict = dotenv_values(".env")
    # Изменить IP в HTML
    html_file = pathlib.Path("./front_vue/public/index.html")
    html_file_prod = pathlib.Path("./front_vue/dist/index.html")

    for file in (html_file, html_file_prod):
        html = file.read_text()
        html = re.sub(
            "const IP_ADR = `[^`]+", f"const IP_ADR = `{env_dict['IP_ADR']}", html
        )
        html = re.sub(
            "const HOST_PORT_DJANGO = `[^`]+",
            f"const HOST_PORT_DJANGO = `{env_dict['HOST_PORT_DJANGO']}",
            html,
        )
        file.write_text(html)
        print("Успешная сборка HTML")


def get_folder_sha256(folder_path: pathlib.Path):
    """
    Получить sha265 папки

    # Пример использования
    folder_path = pathlib.Path('front_vue')
    folder_sha256 = get_folder_sha256(folder_path)
    print(f"SHA-256 хэш папки: {folder_sha256}")
    """
    sha256_hash = hashlib.sha256()

    for root, dirs, files in os.walk(str(folder_path)):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def runAnsibleScript(ctx, limit: str, path_script: str):
    """Выполнить указанный ansible скрипт

    limit: Ограничить выполннение только для указных серверов, если указать `all`, то выполнится для всех
    """
    with ctx.cd("ansible"):
        if limit == "all":
            ctx.run(
                f"{ANSIBLE_HIDE_SKIP} ansible-playbook -i inventory.yml {path_script}"
            )
        else:
            ctx.run(
                f"{ANSIBLE_HIDE_SKIP} ansible-playbook -i inventory.yml {path_script} --limit {limit}"
            )


prod_namespace = Collection()
prod_namespace.add_task(publish)
prod_namespace.add_task(dump)
prod_namespace.add_task(deletePgdata)
prod_namespace.add_task(testDjango)

dck_namespace = Collection()
dck_namespace.add_task(run)
dck_namespace.add_task(restart)
dck_namespace.add_task(down)
dck_namespace.add_task(build)
dck_namespace.add_task(logs)
dck_namespace.add_task(buildVueIfNotExist)

mv_namespace = Collection()
mv_namespace.add_task(ConfToRoot)
mv_namespace.add_task(RootToConf)

namespace = Collection()
namespace.add_collection(prod_namespace, name="prod")
namespace.add_collection(dck_namespace, name="dck")
namespace.add_collection(mv_namespace, name="mv")

# if __name__ == "__main__":
#     ctx = Context()
#     down(ctx, False)
#     print()
