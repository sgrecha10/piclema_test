# piklema_test

## Установка
```
docker-compose build
docker-compose up -d
docker exec -it piklema_test_django ./manage.py migrate
```

### Data migrations
1. Дата миграция (0002) создает пользователя root:123
2. Дата миграция (0003) создается несколько устройств и тегов

## Как пользоваться
### Запустить consumer
```
docker exec -it piklema_test_django ./manage.py consumer
```

### Запустить produser (эмулятор устройства)
```
docker exec -it piklema_test_django ./manage.py device_gen
```
1. После запуска в таблицу TagValue будут записываться значения от устройства.
2. Иногда генерируются некорректные устройства или некорректные теги. Логгирование в консоль.
3. В produser есть константа IS_BROKER, можно установить в False. В этом случае данные будут 
лететь через requests, исключая брокера. Производительность сильно падает. Запускать consumer 
в этом режиме не требуется.

## PostgresDB
```
docker restart piklema_test_postgres
docker exec -i piklema_test_postgres su postgres -c "dropdb -U piklema piklema"
docker exec -i piklema_test_postgres su postgres -c "createdb -U piklema -O piklema piklema"
```
