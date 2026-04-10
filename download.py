import requests
import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# У API лимит 10 полей за раз, поэтому делаем 2 запроса
BASE_URL = "https://restcountries.com/v3.1/all"

BATCH_1 = "fields=cca2,name,population,area,region,subregion,capital,flags,flag,independent"
BATCH_2 = "fields=cca2,languages,currencies,landlocked,timezones,unMember"


def fetch_batch(fields):
    # делаем запрос к API и возвращаем список стран
    url = f"{BASE_URL}?{fields}"
    logger.info("Fetching data...")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_country(c1, c2):
    # Собираем одну строку из двух батчей
    return {
        "cca2": c1.get("cca2"),
        "name": c1.get("name", {}).get("common"),
        "name_full": c1.get("name", {}).get("official"),
        "population": c1.get("population"),
        "area_km2": c1.get("area"),
        "region": c1.get("region"),
        "subregion": c1.get("subregion"),
        "capital": ", ".join(c1.get("capital") or []),
        "flag_emoji": c1.get("flag"),
        "flag_png": c1.get("flags", {}).get("png"),
        "independent": c1.get("independent"),
        # из второго батча
        "languages": ", ".join((c2.get("languages") or {}).values()),
        "currencies": ", ".join((c2.get("currencies") or {}).keys()),
        "landlocked": c2.get("landlocked"),
        "timezones": ", ".join(c2.get("timezones") or []),
        "un_member": c2.get("unMember"),
    }


def build_dataframe():
    batch1 = fetch_batch(BATCH_1)
    batch2 = fetch_batch(BATCH_2)

    # индексируем по cca2 чтобы не делать цикл в цикле
    b2_index = {c["cca2"]: c for c in batch2}

    rows = []
    for country in batch1:
        code = country.get("cca2")
        b2 = b2_index.get(code, {})  # если вдруг нет - пустой словарь
        rows.append(parse_country(country, b2))

    df = pd.DataFrame(rows)
    logger.info("данные загружены")
    return df


def save_to_db(df):
    # подключаемся к базе
    engine = create_engine("postgresql://postgres:postgres@localhost:5433/countries")

    # записываем датафрейм в таблицу
    # если таблица уже есть, пересоздаём
    df.to_sql("countries", con=engine, if_exists="replace", index=False)

    print("данные записаны в базу")

if __name__ == "__main__":
    df = build_dataframe()
    print(df.head())
    print(df.dtypes)
    save_to_db(df)
