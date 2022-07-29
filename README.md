# TEST_Q project

Этот проект было написано специально для компаний КаналСервис для первого этапа собиседование

Исползовано:
- Python 3.9
- Django 4.0.6
- Celery
- Flower
- Postgres
- Redis
- Docker

## Инструкция по установке

После клонирование репозиторий из github-а вам потребуется [Docker](https://docker.com/) для запуска.

После установки Docker:
1. Переходите на директорию с файлом `Dockerfile` внутри репозиторий и запустите следующую команду в камандной страке.
    ```bash
    docker build -t test_q .
    ```
2. Переходите на файл .env.dev и поменйте следйишие переменние:
- `BOT_TOKEN` - если у вас уже есть телеграм бот которому вы хотите подключит систему. Но оно уже имеет бота созданне разработчиком. [aasd_test_bot](https://t.me/aasd_test_bot)
- `TELEGRAM_USER_ID`- поменяте на свой [_**telegram_id**_](https://perfluence.net/blog/article/kak-uznat-id-telegram). Это обязателний иначе система не будет знат каму отправит собшение.
3. Активируют ваш телеграм бот. [aasd_test_bot](https://t.me/aasd_test_bot)
4. Переходите на директорию с файлом `docker-compose.yml` внутри репозиторий и запустите следующую команду в камандной страке.
    ```bash
    docker compose up
    ```
После этого у вас должно запустится проект

## Инструкция по использованию

Все проста система само обновляет и курс и данные каждую минуту вам толко надо увидит резултат.

Также обновляется и курс валюты каждий ден 8 утра

Имеется front-end по адресу - [localhost:8000](https://localhost:8000)
Имеется Flower для маниторинга задач [celery](https://docs.celeryq.dev/en/stable/index.html) по адресу - [localhost:3000](https://localhost:3000)

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)