# TODO

-   [+] Научиться логированию, написать документацию об этом
-   [+] Исправить `publush.yml` так чтобы он сначала копировал проект из git а потом сихранизировал папки с локальной машины
-   [+] Написать тесты API Django, просто хотя бы для того чтобы сверять Json структуры

-   Сделать более удобную форму создания места,

    -   [+] Сделать авто обновление карты после успешного создания нового места
    -   [....-> В процессе] Сделать удаление места
    -   Сделать обновление данных о месте
    -   Вынести input в отдельные компонеты, добавить валидацию поле в компонеты

-   [Отложить эту задачу пока не сделан основной функционал] Jenkins
    -   Настроить авто запуск тестов
    -   Настроить диплой на прод после успешного завершения тестов

# Про диплой

## Зависимости для invoke

```bash
pip install python-dotenv invoke PyYAML
```

## Запустить диплой

```bash
invoke prod.publish --limit=all
```

## Получать Dump базы с прода

```bash
invoke prod.dump --limit=all
```

# Про docker-compose

Запустить контейнеры в `Dev` режиме. В этом режиме только создается Django но не запускается, запускать нужно вручную из контейнера. Такой вариант дает возможность запускать Django в режиме отладки.

```bash
invoke dck.restart --echo
```

Запустить контейнеры в `Prod` режиме

```bash
invoke dck.restart --prod --echo
```
