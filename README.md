# Assistant Bot - Персональний асистент для управління контактами та нотатками

Консольний асистент-бот для управління контактами з підтримкою телефонів, email, адрес, днів народження та нотатками з тегами.

## Встановлення з TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple assistant-bot-G30
```

## Запуск

Після встановлення запустіть бота командою:

```bash
assistant-bot-G30
```

За замовчуванням дані зберігаються у форматі Pickle. Для використання JSON:

```bash
assistant-bot-G30 json
```

## Встановлення з GitHub

```bash
git clone git@github.com:valeriandema/project-group-30.git
cd project-group-30
pip install -r requirements.txt
python main.py
```

Або з вибором формату збереження:

```bash
python main.py json
```

## Основні можливості

✅ Управління контактами (телефони, email, адреси, дні народження)  
✅ Нотатки з тегами та пошуком  
✅ Нечіткий пошук контактів  
✅ Інтерактивний інтерфейс з автодоповненням  
✅ Форматовані таблиці (rich)  
✅ Збереження у Pickle або JSON  

## Команди

### Управління контактами
- `add` - Додати новий контакт (інтерактивний режим з підказками)
- `show` - Показати конкретний контакт (інтерактивний режим)
- `all` - Показати всі контакти у форматованій таблиці
- `search-contacts` - Пошук контактів (інтерактивний режим, підтримка нечіткого пошуку)
- `rename` - Перейменувати контакт (інтерактивний режим)
- `delete` - Видалити контакт (інтерактивний режим з підтвердженням)
- `change` - Змінити поля контакту (інтерактивне меню: ім'я, телефон, email, адреса, день народження)
- `delete-phone` - Видалити телефон з контакту (інтерактивний режим)
- `birthdays <days>` - Показати контакти з днями народження протягом вказаної кількості днів

### Управління нотатками
- `note-add` або `na` - Додати нову нотатку (інтерактивний режим)
- `note-list` або `nl` - Показати список нотаток з можливістю пошуку
- `note-edit` або `ne` - Редагувати нотатку (інтерактивний режим)
- `note-del` або `nd` - Видалити нотатку (інтерактивний режим)
- `tag` - Показати нотатки згруповані за тегами

### Інше
- `help` - Показати всі команди у форматованій таблиці
- `exit` / `quit` / `close` - Вийти з програми

## Приклад використання

```bash
# Додати контакт
> add
Name (required): John Doe
Phone (optional) [380XXXXXXXXX]: 380501234567
Email (optional): john@example.com

# Пошук
> search-contacts
Query string: john

# Змінити дані (інтерактивне меню)
> change

# Нотатки
> note-add
Enter note text: Купити молоко
Enter tags: покупки, продукти

> tag  # Показати за тегами
```

## Структура проекту

```
project-group-30/
├── cli/                        # CLI компоненти
│   ├── presenter.py            # Форматований вивід (colorama, rich)
│   ├── command_suggester.py    # Підказки команд
│   ├── prompt_manager.py       # Управління вводом (prompt_toolkit)
│   ├── table_renderer.py       # Рендеринг таблиць
│   └── styles.py               # Стилі для інтерфейсу
├── handlers/                   # Обробники команд
│   ├── command_handler.py      # Основний обробник команд
│   ├── birthday_service.py     # Сервіс для роботи з днями народження
│   ├── decorators.py           # Декоратори для обробки помилок
│   └── errors.py               # Кастомні помилки
├── models/                     # Моделі даних
│   ├── contact.py              # Record (контакт)
│   ├── name.py                 # Name (ім'я)
│   ├── phone.py                # Phone (телефон)
│   ├── email.py                # Email
│   ├── address.py              # Address (адреса)
│   ├── birthday.py             # Birthday (день народження)
│   ├── note.py                 # Note (нотатка)
│   └── field.py                # Field (базове поле)
├── repositories/               # Репозиторії
│   └── contact_repository.py   # Репозиторій контактів та нотаток
├── storage/                    # Збереження даних
│   ├── factory.py              # Фабрика для створення storage
│   ├── pickle_storage.py       # Pickle збереження
│   └── json_storage.py         # JSON збереження
├── search/                     # Пошук
│   └── search_service.py       # Сервіс пошуку з нечітким пошуком
├── utils/                      # Утиліти
│   └── utils.py                # Допоміжні функції
├── files/                      # Файли даних (створюється автоматично)
├── main.py                     # Точка входу
├── setup.py                    # Конфігурація для PyPI
├── pyproject.toml              # Сучасна конфігурація пакету
└── requirements.txt            # Залежності
```

## Вимоги

- Python 3.8 або вище
- colorama - кольоровий вивід у консолі
- rich - форматовані таблиці та текст
- prompt_toolkit - автодоповнення та історія команд

## Розробка

```bash
git clone https://github.com/LesDevLabs/project-group-30.git
cd project-group-30
python -m venv venv
venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
python main.py  # або: python main.py json
```

## Ліцензія

MIT License

## Автори

Group 30 (2025)
- Sagepol
- 444ten
- Koliaepov
- Valerian Demichev
- Zarudenska
- lestyshchenko
