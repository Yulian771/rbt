import datetime as dt
import pandas as pd
from func.func import YouTubeApi, TelegramNotification, LoadData

from airflow import DAG
from airflow.operators.python_operator import PythonOperator



# Google API
youtube_access_token = '#REPLACE#'
channel_id = '#REPLACE#'

# DB
conn_id = '#REPLACE#'
table = '#REPLACE#'
schema = '#REPLACE#'

# TG Notification
bot_token = '#REPLACE#'
chat_token = '#REPLACE#'


def work_with_data(youtube_access_token: str, channel_id: str, conn_id: str, table: str, schema: str, bot_token: str,
                   chat_token: str):
    # Get Data from YouTube API
    youtube_data = YouTubeApi(youtube_access_token, channel_id)
    df = youtube_data.get_stat()

    # Send Data To DB
    loader = LoadData(df, conn_id, table, schema)
    loader.send_data()

    # Send TG Notification
    tg_sender = TelegramNotification(bot_token, chat_token, df)
    tg_sender.send_tg_message()





default_args = {
    'owner': 'rbt',
    'start_date': dt.datetime(2023, 2, 17),
    'retries': 3,
    'retry_delay': dt.timedelta(minutes=10),
}

with DAG('Get_YouTube_Data',
         default_args=default_args,
         schedule_interval='0 15 * * *',
         catchup=False,
         ) as dag:
    main_task = PythonOperator(task_id='get_youtube_data',
                                     python_callable=work_with_data,
                                     op_kwargs={'youtube_access_token': youtube_access_token,
                                                'channel_id': channel_id,
                                                'conn_id': conn_id,
                                                'table': table,
                                                'schema': schema,
                                                'bot_token': bot_token,
                                                'chat_token': chat_token})


main_task
