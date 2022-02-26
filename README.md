# Homework-48

Для запуска проекта установите python версии 3.9 и выше и pip

После клонирования перейдите в склонированную папку и выполните следующие команды:

Создайте виртуальное окружение командой
```bash
python -m venv venv
```

Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
или
venv\Scripts\activate
```

Установите зависимости командой

```bash
pip install -r requirements.txt
```

Примените миграции командой
```bash
./manage.py migrate
```

Загрузите фикстурные статьи командой
```bash
1) ./manage.py loaddata auth_dump.json
2) ./manage.py loaddata dump.json
```

Чтобы запустить сервер выполните:

```bash
./manage.py runserver
```

Для доступа в панель администратора перейдите по ссылке http://localhost:8000/admin
