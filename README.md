## Деплой

Тестовое задание доступно по адресу: https://django-stripe-test-qxz7.onrender.com
Админ панель: https://django-stripe-test-qxz7.onrender.com/admin
Логин и пароль: admin admin

## Структура проекта

```
stripe_project/
├── manage.py                 # Django управляющий скрипт
├── requirements.txt          # Python зависимости
├── .env                      # Переменные окружения (включён в репозиторий)
├── Dockerfile                # Docker конфигурация
├── docker-compose.yml        # Docker Compose настройки
├── db.sqlite3                # База данных SQLite
├── stripe_project/           # Основной проект
│   ├── settings.py           # Настройки Django
│   ├── urls.py               # URL маршруты
│   └── wsgi.py               # WSGI конфигурация
├── payments/                 # Приложение платежей
│   ├── models.py             # Модели данных
│   ├── views.py              # Представления
│   ├── urls.py               # URL маршруты приложения
│   ├── templates/            # HTML шаблоны
│   └── migrations/           # Миграции базы данных
└── static/                   # Статические файлы
    └── css/
        └── style.css         # Стили
```

## Модели данных

- **Item** - Товары с названием, описанием, ценой и валютой
- **Order** - Заказы, содержащие товары со скидками и налогами
- **OrderItem** - Связующая модель между заказами и товарами
- **Discount** - Скидки с автоматическим созданием купонов в Stripe
- **Tax** - Налоги с интеграцией Stripe Tax Rates

## Установка и запуск

### Предварительные требования

- Python 3.8+
- Аккаунт Stripe с API ключами
- Docker (опционально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/kitaychyo/django-stripe-test.git
cd stripe_project
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## Запуск через Docker

### Простой запуск

```bash
docker-compose up --build
```

### Запуск в фоновом режиме

```bash
docker-compose up -d --build
```

### Остановка контейнеров

```bash
docker-compose down
```

## Использование

### Основные страницы

- `/` - Главная страница со списком товаров и заказов
- `/item/<id>/` - Детальная страница товара с кнопкой покупки
- `/order/<id>/` - Детальная страница заказа с кнопкой оплаты
- `/success/` - Страница успешной оплаты
- `/cancel/` - Страница отмененной оплаты
- `/admin/` - Административная панель Django

### API эндпоинты

- `GET /buy/<item_id>/` - Создание Stripe Checkout сессии для товара
- `GET /buy-order/<order_id>/` - Создание Stripe Checkout сессии для заказа

## Тестирование

### Тестовые карты Stripe

Для тестирования используйте тестовые номера карт Stripe:

- **Успешная оплата:** 4242 4242 4242 4242
- **Отклоненная карта:** 4000 0000 0000 0002
- **Требуется аутентификация:** 4000 0025 0000 3155

Любая будущая дата и CVC код для тестовых карт.

