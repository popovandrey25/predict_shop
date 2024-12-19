from prefect import flow, task
from prefect.schedules import IntervalSchedule
from datetime import timedelta, datetime

from ETL import ETL

def run_etl():
    db_uri = 'postgresql://username:password@localhost:5432/mydatabase'
    output_file = f'data_{datetime.now().strftime("%Y%m%d")}.csv'

    etl = ETL(db_uri, output_file)
    etl.run()

@task
def execute_etl():
    run_etl()

@flow(schedule=IntervalSchedule(interval=timedelta(days=1)))  # Запуск раз в день
def etl_flow():
    execute_etl()
