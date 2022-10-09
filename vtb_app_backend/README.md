



## Запуск сервисов (бекенд)

```
git clone git@gitlab.com:itaidi/vtb_app.git
cd vtb_app
docker-compose up

```

## Настройки

Настройки прописаны в этих файлах
```

# обычно этот файл настраивается на сервере, но так как mvp проект, все данные установлены
nano app/.env

# файл образец настроек
nano app/def.env

```

## документация (Postman)

Url [https://documenter.getpostman.com/view/23758491/2s83zgv5QL](https://documenter.getpostman.com/view/23758491/2s83zgv5QL)

Json [https://www.getpostman.com/collections/cf932535d433762f923b](https://www.getpostman.com/collections/cf932535d433762f923b)

docs/

```
Envionment (Postman):

authService = http://localhost:3001

TEST_EVENT_ID = "6341f8ec0af2f78f713cd2db"
TEST_EVENT_USER_ID = 102

```


