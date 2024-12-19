import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
class ETL:
    def __init__(self, db_uri, output_file):
        """
        Инициализация класса ETL.

        :param db_uri: URI подключения к базе данных PostgreSQL.
        :param query: SQL-запрос для извлечения данных.
        :param output_file: Путь к файлу, в который будут сохранены извлеченные данные.
        """
        self.db_uri = db_uri
        self.output_file = output_file
        self.data = None

    def extract(self):
        """
        Извлечение данных из базы данных.
        """
        try:
            engine = create_engine(self.db_uri)
            self.data = pd.read_sql(self.query, engine)
            print("Данные успешно извлечены.")
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")

    def transform(self):
        """
        Преобразование данных.
        Здесь можно добавить свою логику преобразования.
        """
        pass

    def load(self):
        """
        Загрузка данных в файл.
        """
        pass

    def run(self):
        """
        Запуск процесса ETL.
        """
        self.extract()
        self.transform()
        self.load()