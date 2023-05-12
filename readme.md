# Про диплой

## Зависимости для invoke

```bash
pip install python-dotenv invoke
```

## Запустить диплой

```bash
invoke prod.publish
```

## Получать Dump базы с прода

```bash
invoke prod.dump
```

# Про docker-compose

Запустить контейнеры в `Dev` режиме

```bash
invoke dck.restart
```

Запустить контейнеры в `Prod` режиме

```bash
invoke dck.restart --prod
```
