# data-download-pipeline

Пайплайн загружает данные о странах через API и показывает их в дашборде.

## Как запустить

### 1. Установить зависимости
```
pip install -r requirements.txt
```

### 2. Запустить базу данных
```
docker compose up -d
```

### 3. Загрузить данные
```
python download.py
```

### 4. Запустить дашборд
```
python visualization.py
```

Открыть в браузере http://127.0.0.1:8050


## Стек
- Python, pandas, requests
- PostgreSQL в Docker
- Dash для визуализации

## Примечания
PostgreSQL запускается на порту 5433 а не на стандартном 5432, чтобы не конфликтовать с локальной установкой Postgre.
