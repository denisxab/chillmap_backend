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

######################
# Для диплой


@task
def publish(ctx):
    """Отправить проект на прод"""
    # Перед диплоем, собрать Vue.js приложение в контейнере
    ctx.run(f"docker build -t dockerfile_vue_prod -f {DOCKERFILE_VUE_BUILD} .")
    ctx.run("docker run -v ./front_vue:/app -v /app/node_modules dockerfile_vue_prod")
    # Выполнить диплой
    with ctx.cd("ansible"):
        ctx.run("ansible-playbook -i inventory.yml publush.yml")


@task
def dump(ctx):
    """Сделать дамб базы на проде, и копировать её на текущую машину
    в ./backend/fixtures/api.json"""
    with ctx.cd("ansible"):
        ctx.run("ansible-playbook -i inventory.yml dump_api.yml")


######################
# Взаимодействие с docker-compose


@task
def run(ctx, prod, detach):
    """Запустить docker-compose"""
    ConfToRoot(ctx, prod)
    build_html()
    ctx.run(
        f"docker-compose -f ./docker-compose.yml up {'-d' if detach == 'True' else ''} app db nginx_vue nginx_static"
        if prod == "True"
        else "docker-compose -f ./docker-compose.yml up"
    )
    RootToConf(ctx)


@task
def restart(ctx, prod, detach):
    """Перезапустить docker-compose"""
    down(ctx, prod)
    build(ctx, prod)
    run(ctx, prod, detach)


@task
def down(ctx, prod):
    """Остановить docker-compose"""
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml down")
    RootToConf(ctx)


@task
def build(ctx, prod):
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml build")
    RootToConf(ctx)


@task
def logs(ctx, prod):
    """Посмотреть логи"""
    ConfToRoot(ctx, prod)
    ctx.run("docker-compose logs")
    RootToConf(ctx)


######################
# Перенеиспользуемые задачи


@task
def ConfToRoot(ctx, prod):
    shutil.copyfile(
        DOCKERFILE_DJANGO_PROD if prod == "True" else DOCKERFILE_DJANGO_DEV,
        DOCKERFILE_DJANGO,
    )


@task
def RootToConf(ctx):
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
