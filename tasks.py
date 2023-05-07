import os

from invoke import task

# Конфигурация для разработки
file_dev = [
    ".env",
    "docker-compose_dev.yml",
    "Dockerfile_Django",
    "Dockerfile_Vue",
    "nginx.conf",
]


@task
def mvDevToRoot(ctx):
    try:
        for file in file_dev:
            os.rename(f"./dev_conf/{file}", f"./{file}")
    except FileNotFoundError:
        ...


@task
def mvRootToDev(ctx):
    try:
        for file in file_dev:
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
    ctx.run("docker-compose -f ./docker-compose_dev.yml up")
    mvRootToDev(ctx)


@task
def downDev(ctx):
    mvDevToRoot(ctx)
    ctx.run("docker-compose -f ./docker-compose_dev.yml down")
    mvRootToDev(ctx)
