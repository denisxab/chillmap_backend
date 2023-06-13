import os
from invoke import Collection, task, Runner


from devops.invoke_code import (
    LIST_DEV_APP,
    LIST_PROD_APP,
    LIST_TEST_DJANGO_APP,
    ConfToRoot,
    RootToConf,
    build_html,
    buildVueIfNotExist,
    runAnsibleScript,
)


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
    print("::::::::::::Запуск docker-compose::::::::::::")
    restart(ctx, prod=prod, detach=True, list_prod_app=LIST_TEST_DJANGO_APP)
    print("::::::::::::Выполнение теста::::::::::::")
    command = "pytest"
    ctx.run(f"docker-compose exec app {command}", pty=True)


######################
# Взаимодействие с docker-compose


@task
def build(ctx, prod=False, list_prod_app: str = ""):
    """Собрать docker-compose"""
    ConfToRoot(ctx, prod)
    if prod and not list_prod_app:
        list_prod_app = LIST_PROD_APP
    if not prod and not list_prod_app:
        list_prod_app = LIST_DEV_APP
    ctx.run(f"docker-compose build {list_prod_app}", pty=True)
    RootToConf(ctx)


@task
def run(ctx, prod=False, detach=False, list_prod_app: str = ""):
    """Запустить docker-compose"""
    ConfToRoot(ctx, prod)
    build_html()
    if prod and not list_prod_app:
        list_prod_app = LIST_PROD_APP
    if not prod and not list_prod_app:
        list_prod_app = LIST_DEV_APP
    ctx.run(f"docker-compose up {'-d' if detach else ''} {list_prod_app}", pty=True)
    RootToConf(ctx)


@task
def restart(ctx, prod=False, detach=False, list_prod_app: str = ""):
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
# Для SSL
@task
def ssl_create(ctx: Runner):
    """Создать SSL сертификаты для работы пл HTTPS"""
    with ctx.cd("./devops"):
        ctx.run("mkdir -p ./ssl")
        # Если уже есть сертификаты то не удаляем их !
        if (
            len(
                {"certificate.crt", "private_key"}.intersection(
                    set(ctx.run("ls ./ssl").stdout.split("\n"))
                )
            )
            == 2
        ):
            raise FileExistsError("Сертификаты уже созданы !")
        else:
            ctx.run(
                "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./ssl/private_key -out ./ssl/certificate.crt -subj '/C=RU'"
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

ssl_namespace = Collection()
ssl_namespace.add_task(ssl_create, "create")

namespace = Collection()
namespace.add_collection(prod_namespace, name="prod")
namespace.add_collection(dck_namespace, name="dck")
namespace.add_collection(mv_namespace, name="mv")
namespace.add_collection(ssl_namespace, name="ssl")

# if __name__ == "__main__":
#     ctx = Context()
#     down(ctx, False)
#     print()
