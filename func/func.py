import datetime
import requests
import pandas as pd
from datetime import timedelta
from sqlalchemy import create_engine

from airflow.providers.odbc.hooks.odbc import OdbcHook


class YouTubeApi:
    def __init__(self, access_token: str, channel_id: str) -> None:
        self.access_token = access_token
        self.channel_id = channel_id

    def _videos(self):
        query_ts = datetime.datetime.now(datetime.timezone.utc) - timedelta(hours=24)
        query_ts = query_ts.strftime("%Y-%m-%dT%H:%M:%SZ")

        endp_search = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=50&order=date&publishedAfter={query_ts}&type=video&key={access_token}'.format(
            channel_id=self.channel_id,
            query_ts=query_ts,
            access_token=self.access_token)
        result = dict()

        try:
            response = requests.get(endp_search)
            data = response.json()

            for i in data['items']:
                id = i['id']['videoId']
                t = i['snippet']['title']
                p = i['snippet']['publishedAt']
                result[id] = {'title': t, 'publishedAt': p}

        except requests.exceptions.RequestException as err:
            print(err)

        return result

    def get_stat(self):
        result_list = []
        videos_data = self._videos()

        if len(videos_data) != 0:
            for key, value in videos_data.items():
                endp_stat = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={access_token}'.format(
                    video_id=key,
                    access_token=self.access_token)

                try:
                    response = requests.get(endp_stat)
                    data = response.json()

                    for x in data['items']:
                        stat = x['statistics']
                        stat['url'] = 'https://www.youtube.com/watch?v=' + str(key)
                        stat['title'] = value['title']
                        stat['publishedAt'] = value['publishedAt']
                        result_list.append(stat)

                except requests.exceptions.RequestException as err:
                    print(err)

        return pd.DataFrame(result_list)


class TelegramNotification:
    def __init__(self, bot_token: str, chat_token: str, df: pd.DataFrame()) -> None:
        self.bot_token = bot_token
        self.chat_token = chat_token
        self.df = df

    def send_tg_message(self):
        df = self.df.astype({"viewCount": int})
        df = df.sort_values(by=['viewCount'], ascending=False).reset_index(). \
            drop(columns=['favoriteCount', 'publishedAt']).head(5)

        line = "Топ роликов за прошедший день"
        for i in range(0, len(df)):
            title = str(df['title'][i])
            views = 'Просмотров: ' + str(df['viewCount'][i])
            likes = 'Лайков: ' + str(df['likeCount'][i])
            comments = 'Комментариев: ' + str(df['commentCount'][i])
            url = str(df['url'][i])
            line = line + "\n" + "\n" + "Ролик #" + str(
                i + 1) + "\n" + "\n" + title + "\n" + views + "\n" + likes + "\n" + comments + "\n" + url

        requests.post(
            'https://api.telegram.org/' +
            'bot{}/sendMessage'.format(self.bot_token),
            params=dict(chat_id=self.chat_token, text=f"<b>{line}</b>", parse_mode='HTML')
        )


class LoadData:
    def __init__(self, df: pd.DataFrame(), conn_str: str, table: str, schema: str) -> None:
        self.df = df
        self.conn_str = conn_str
        self.table = table
        self.schema = schema

    def send_data(self):
        conn = OdbcHook(self.conn_str)
        eng = create_engine(conn.get_uri())

        if len(self.df) != 0:
            self.df.to_sql(self.table, schema=self.schema, index=False, con=eng, if_exists='append')