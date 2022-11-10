# piklema_test

```
docker restart piklema_test_postgres
docker exec -i piklema_test_postgres su postgres -c "dropdb -U piklema piklema"
docker exec -i piklema_test_postgres su postgres -c "createdb -U piklema -O piklema piklema"
```
