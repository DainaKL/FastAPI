Как запустить проект
 1. Создание виртуального окружения
python -m venv venv
 2. Активация виртуального окружения
venv\Scripts\activate
 3. Установка зависимостей
pip install -r requirements.txt
 4. Запуск миграций Alembic
alembic upgrade head
 5. Создание первого администратора
python create_first_admin.py
 7. Запуск приложения
python main.py
Запуск через Docker
docker-compose up --build
 Данные для входа админа
- Логин: `admin`
- Пароль: `admin123`