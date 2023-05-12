import os
import pathlib
import re
import shutil
from contextlib import suppress

from dotenv import dotenv_values
from invoke import Context, task, Collection

FILE_DEV = [
    ".env",
    "nginx.conf",
]

DOCKERFILE_DJANGO_DEV = "./dev_conf/Dockerfile_Django_Dev"
DOCKERFILE_DJANGO_PROD = "./dev_conf/Dockerfile_Django_Prod"
DOCKERFILE_DJANGO = "./Dockerfile_Django"
DOCKERFILE_VUE_DEV = "./dev_conf/Dockerfile_Vue_Dev"
DOCKERFILE_VUE_PROD = "./dev_conf/Dockerfile_Vue_Prod"
DOCKERFILE_VUE = "./Dockerfile_Vue"

FILE_ALL = [
    ".env",
    DOCKERFILE_DJANGO_DEV,
    DOCKERFILE_DJANGO_PROD,
    DOCKERFILE_VUE_DEV,
    DOCKERFILE_VUE_PROD,
    "nginx.conf",
]

######################
# Для диплой


@task
def publish(ctx):
    """Отправить проект на прод"""
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
def run(ctx, prod):
    """Запустить docker-compose"""
    DevToRoot(ctx, prod)
    build_html()
    ctx.run(
        "docker-compose -f ./docker-compose.yml up -d"
        if prod
        else "docker-compose -f ./docker-compose.yml up"
    )
    RootToDev(ctx)


@task
def restart(ctx, prod):
    """Перезапустить docker-compose"""
    down(ctx, prod)
    run(ctx, prod)


@task
def down(ctx, prod):
    """Остановить docker-compose"""
    DevToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml down")
    RootToDev(ctx)


@task
def build(ctx, prod):
    DevToRoot(ctx, prod)
    ctx.run("docker-compose -f ./docker-compose.yml build")
    RootToDev(ctx)


######################
# Перенеиспользуемые задачи


@task
def DevToRoot(ctx, prod):
    print("Prod: ", prod)
    shutil.copyfile(
        DOCKERFILE_DJANGO_PROD if prod else DOCKERFILE_DJANGO_DEV, DOCKERFILE_DJANGO
    )
    shutil.copyfile(DOCKERFILE_VUE_PROD if prod else DOCKERFILE_VUE_DEV, DOCKERFILE_VUE)
    for file in FILE_DEV:
        with suppress(FileNotFoundError):
            os.rename(f"./dev_conf/{file}", f"./{file}")


@task
def RootToDev(ctx):
    with suppress(FileNotFoundError):
        os.remove(DOCKERFILE_DJANGO)
    with suppress(FileNotFoundError):
        os.remove(DOCKERFILE_VUE)
    for file in FILE_ALL:
        with suppress(FileNotFoundError):
            os.rename(f"./{file}", f"./dev_conf/{file}")


######################
# Утилиты


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


prod_namespace = Collection()
prod_namespace.add_task(publish)
prod_namespace.add_task(dump)

dck_namespace = Collection()
dck_namespace.add_task(run)
dck_namespace.add_task(restart)
dck_namespace.add_task(down)
dck_namespace.add_task(build)

mv_namespace = Collection()
mv_namespace.add_task(DevToRoot)
mv_namespace.add_task(RootToDev)

namespace = Collection()
namespace.add_collection(prod_namespace, name="prod")
namespace.add_collection(dck_namespace, name="dck")
namespace.add_collection(mv_namespace, name="mv")

# if __name__ == "__main__":
#     ctx = Context()
#     down(ctx, False)
#     print()
