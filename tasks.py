import os
import pathlib
import re
import shutil
from contextlib import suppress

from dotenv import dotenv_values
from invoke import Context, task

FILE_DEV = [
    ".env",
    "Dockerfile_Vue",
    "nginx.conf",
]

FILE_ALL = [
    ".env",
    "Dockerfile_Django_Dev",
    "Dockerfile_Django_Prod",
    "Dockerfile_Vue",
    "nginx.conf",
]
DOCKERFILE_DJANGO_DEV = "./dev_conf/Dockerfile_Django_Dev"
DOCKERFILE_DJANGO_PROD = "./dev_conf/Dockerfile_Django_Prod"
DOCKERFILE_DJANGO = "./Dockerfile_Django"


@task
def mvDevToRoot(ctx, prod):
    shutil.copyfile(
        DOCKERFILE_DJANGO_PROD if prod else DOCKERFILE_DJANGO_DEV, DOCKERFILE_DJANGO
    )
    for file in FILE_DEV:
        with suppress(FileNotFoundError):
            os.rename(f"./dev_conf/{file}", f"./{file}")


@task
def mvRootToDev(ctx):
    with suppress(FileNotFoundError):
        os.remove(DOCKERFILE_DJANGO)
    for file in FILE_ALL:
        with suppress(FileNotFoundError):
            os.rename(f"./{file}", f"./dev_conf/{file}")


@task
def build(ctx, prod):
    mvDevToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml build")
    mvRootToDev(ctx)


@task
def run(ctx, prod):
    """Запустить docker-compose"""
    mvDevToRoot(ctx, prod)
    build_html()
    ctx.run(
        "docker-compose -f ./docker-compose.yml up -d"
        if prod
        else "docker-compose -f ./docker-compose.yml up"
    )
    mvRootToDev(ctx)


@task
def restart(ctx, prod):
    """Перезапустить docker-compose"""
    down(ctx, prod)
    run(ctx, prod)


@task
def down(ctx, prod):
    """Остановить docker-compose"""
    mvDevToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml down")
    mvRootToDev(ctx)


@task
def publish(ctx):
    """Отправить проект на прод"""
    with ctx.cd("ansible"):
        ctx.run("ansible-playbook -i inventory.yml publush.yml")


@task
def getDump(ctx):
    """Сделать дамб базы на проде, и копировать её на текущую машину
    в ./backend/fixtures/api.json"""
    with ctx.cd("ansible"):
        ctx.run("ansible-playbook -i inventory.yml dump_api.yml")


######################


def build_html():
    env_dict = dotenv_values(".env")
    # Изменить IP в HTML
    html_file = pathlib.Path("./front_vue/public/index.html")
    html = html_file.read_text()
    html = re.sub(
        "const IP_ADR = `[^`]+", f"const IP_ADR = `{env_dict['IP_ADR']}", html
    )
    html = re.sub(
        "const HOST_PORT_DJANGO = `[^`]+",
        f"const HOST_PORT_DJANGO = `{env_dict['HOST_PORT_DJANGO']}",
        html,
    )
    html_file.write_text(html)
    print("Успешная сборка HTML")


# if __name__ == "__main__":
#     ctx = Context()
#     down(ctx, False)
#     print()
