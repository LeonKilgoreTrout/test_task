# Тестовое задание

### Локальный запуск

1) prerequisites: MongoDB, python 3.11.3
2) изменить в .env переменную DATABASE_URL на "mongodb://localhost:27017"
Находясь в корне проекта
3) Установить зависимости в заранее созданном окружении
``` poetry install ```
или
``` pip install -r requirements.txt ```
4) прогнать тесты если необходимо командой ```pytest```
5) добавить тестовые данные:
```commandline
python -m insert_templates
```
6) запустить апи командой
``` uvicorn app.main:app ```

### запуск с Docker
Находясь в корне проекта, выполнить команды

1) 
```
docker build . --no-cache
```
2) 
```
docker compose up
```

Также тестировать запросы можно с помощью Swagger во вкладке docs:

http://localhost:8000/docs



### Конфликт шаблонов

"Полей в пришедшей форме может быть больше чем
в шаблоне, в этом случае шаблон все равно будет
считаться подходящим. Самое главное, чтобы все поля
шаблона присутствовали в форме."

Если будут храниться только такие шаблоны,
```commandline
[
    {
        "name": "some_name_1",
        "owner_email": "email",
        "customer_phone": "phone"
    },
    {
        "name": "some_name_2",
        "owner_email": "email",
        "order_date": "date"
    }
]
```

а на вход придёт такой запрос
```
/get_form/owner_email=some@mail.ru&customer_phone=+79437684343&order_date=31.12.1998"
```

после валидации получим
```
{
    "owner_email": "email",
    "customer_phone": "phone",
    "order_date": "date"
}
```

решил что можно вернуть name обеих форм.


### Конфликт шаблонов (продолжение)
"Самое главное, чтобы все поля
шаблона присутствовали в форме"

Если мы решаем вышеописанный конфликт, то возникает другая ситуация. Когда у нас есть форма:

```
{
    "name": "some_name_2",
    "order_date": "date"
}
```

То ей будут подходить шаблоны с огромным кол-вом полей, например такая:

```commandline

{
    "name": "some_name_2",
    "owner_email": "some@mail.ru",
    "order_date": "31.12.1998",
    "phone": "+7 892 232 2323",
    "plain_text": "Hi!",
    "more_useless_text": "asdassadsa",
    "neighbor_phone": "+7 2322234234"
    ...
    "some_date": "30.12.1998"
}

```