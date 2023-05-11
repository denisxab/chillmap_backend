import os
import pathlib
import re
import shutil

from dotenv import dotenv_values
from invoke import task

# Конфигурация для разработки
file_dev = [
    ".env",
    "docker-compose.yml",
    "Dockerfile_Vue",
    "nginx.conf",
]

file_all = [
    ".env",
    "docker-compose.yml",
    "Dockerfile_Django_Dev",
    "Dockerfile_Django_Prod",
    "Dockerfile_Vue",
    "nginx.conf",
]


@task
def mvDevToRoot(ctx, prod=False):
    try:
        if prod:
            shutil.copyfile("./dev_conf/Dockerfile_Django_Prod", "./Dockerfile_Django")
        else:
            shutil.copyfile("./dev_conf/Dockerfile_Django_Dev", "./Dockerfile_Django")
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
    ctx.run("docker-compose -f ./docker-compose.yml build")
    mvRootToDev(ctx)


@task
def buildProd(ctx):
    mvDevToRoot(ctx, prod=True)
    ctx.run("docker-compose -f ./docker-compose.yml build")
    mvRootToDev(ctx)


@task
def runDev(ctx):
    mvDevToRoot(ctx)
    build_html()
    ctx.run("docker-compose -f ./docker-compose.yml up")
    mvRootToDev(ctx)


@task
def runProd(ctx):
    mvDevToRoot(ctx, prod=True)
    build_html()
    ctx.run("docker-compose -f ./docker-compose.yml up -d")
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
    ctx.run("docker-compose -f ./docker-compose.yml down")
    mvRootToDev(ctx)


@task
def downProd(ctx):
    mvDevToRoot(ctx, prod=True)
    ctx.run("docker-compose -f ./docker-compose.yml down")
    mvRootToDev(ctx)
