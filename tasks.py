import os
import pathlib
import re
import shutil
from contextlib import suppress

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

# Скрыть из вывода в консоли задачи который skip
ANSIBLE_HIDE_SKIP = "export ANSIBLE_DISPLAY_SKIPPED_HOSTS=no &&"

######################
# Для диплой


@task
def publish(ctx, limit):
    """Отправить проект на прод

    limit: Ограничить выполннение только дял указных серверов, если указать `all`, то выполнится для всех
    """
    # Сборка Vue.js приложения на локальной машине перед диплоем
    ctx.run(f"docker build -t dockerfile_vue_prod -f {DOCKERFILE_VUE_BUILD} .")
    ctx.run("docker run -v ./front_vue:/app -v /app/node_modules dockerfile_vue_prod")
    ctx.run("sudo chown $USER:$USER -R ./front_vue")
    # Выполнить диплой
    with ctx.cd("ansible"):
        if limit == "all":
            ctx.run(
                f"{ANSIBLE_HIDE_SKIP} ansible-playbook -i inventory.yml publush.yml"
            )
        else:
            ctx.run(
                f"{ANSIBLE_HIDE_SKIP} ansible-playbook -i inventory.yml publush.yml --limit {limit}"
            )


@task
def dump(ctx, limit):
    """Сделать дамб базы на проде, и копировать её на текущую машину
    в ./backend/fixtures/api.json

    limit: Ограничить выполннение только дял указных серверов, если указать `all`, то выполнится для всех
    """
    with ctx.cd("ansible"):
        if limit == "all":
            ctx.run("ansible-playbook -i inventory.yml dump_api.yml")
        else:
            ctx.run(f"ansible-playbook -i inventory.yml dump_api.yml  --limit {limit}")


######################
# Взаимодействие с docker-compose


@task
def run(ctx, prod=False, detach=False):
    """Запустить docker-compose"""
    ConfToRoot(ctx, prod)
    build_html()
    ctx.run(
        f"docker-compose up {'-d' if detach else ''} {LIST_PROD_APP}"
        if prod
        else "docker-compose up"
    )
    RootToConf(ctx)


@task
def restart(ctx, prod=False, detach=False):
    """Перезапустить docker-compose"""
    down(ctx, prod)
    build(ctx, prod)
    run(ctx, prod, detach)


@task
def down(ctx, prod=False):
    """Остановить docker-compose"""
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose down")
    RootToConf(ctx)


@task
def build(ctx, prod=False):
    """Собрать docker-compose"""
    ConfToRoot(ctx, prod)
    ctx.run(f"docker-compose build {LIST_PROD_APP}" if prod else "docker-compose build")
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


prod_namespace = Collection()
prod_namespace.add_task(publish)
prod_namespace.add_task(dump)

dck_namespace = Collection()
dck_namespace.add_task(run)
dck_namespace.add_task(restart)
dck_namespace.add_task(down)
dck_namespace.add_task(build)
dck_namespace.add_task(logs)

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
