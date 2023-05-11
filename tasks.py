import os
import pathlib
import re

from dotenv import dotenv_values
from invoke import task

# Конфигурация для разработки
file_dev = [
    ".env",
    "docker-compose_dev.yml",
    "Dockerfile_Vue",
    "nginx.conf",
]

file_all = [
    ".env",
    "docker-compose_dev.yml",
    "Dockerfile_Django_Dev",
    "Dockerfile_Django_Prod",
    "Dockerfile_Vue",
    "nginx.conf",
]


@task
def mvDevToRoot(ctx, prod=False):
    try:
        if prod:
            os.rename("./dev_conf/Dockerfile_Django_Prod", "./Dockerfile_Django")
        else:
            os.rename("./dev_conf/Dockerfile_Django_Dev", "./Dockerfile_Django")
        for file in file_dev:
            os.rename(f"./dev_conf/{file}", f"./{file}")
    except FileNotFoundError:
        ...


@task
def mvRootToDev(ctx):
    try:
        for file in file_all:
            os.rename(f"./{file}", f"./dev_conf/{file}")
    except FileNotFoundError:
        ...


@task
def buildDev(ctx):
    mvDevToRoot(ctx)
    ctx.run("docker-compose -f ./docker-compose_dev.yml build")
    mvRootToDev(ctx)


@task
def runDev(ctx):
    mvDevToRoot(ctx)
    build_html()
    ctx.run("docker-compose -f ./docker-compose_dev.yml up")
    mvRootToDev(ctx)


@task
def runProd(ctx):
    mvDevToRoot(ctx)
    build_html()
    ctx.run("docker-compose -f ./docker-compose_prod.yml up")
    mvRootToDev(ctx)


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


@task
def downDev(ctx):
    mvDevToRoot(ctx)
    ctx.run("docker-compose -f ./docker-compose_dev.yml down")
    mvRootToDev(ctx)
