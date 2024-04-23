# rbt

Get_YouTube_Data.py и func - DAG <br />
YouTube Report.pbix - файл отчета <br />


# Документация<br />

## Требования<br />
Система должна осуществлять сбор данных о видеороликах опубликованных на платформе YouTube
за последние 24 часа с использованием YouTube Data API. Данные должны включать: название видео,
количество просмотров, количество лайков, количество комментариев.

Ежедневно отправлять уведомление в Telegram с информацией о топ-5 видеороликах с названием,
количеством просмотров, лайков, комментариев и ссылкой на видео.

Система включает в себя отчет PWBI с визуализацией графиков изменения количества просмотров,
лайков и комментариев во времени.

## Реализация<br />
Процесс загрузки данных из источника YouTube Data API в приемник разрабатываемой системы
реализован с помощью DAG-оркестратора Airflow на языке программирования Python.
DAG содержит задачи на соответствующий запрос данных из источника YouTube Data API.
Обработку полученных данных, отправку очищенных данных в приемник, а так же отправку уведомления в Telegram.
Для реализации этого процесса были использованы следующие библиотеки Python:
- requests<br />
- pandas<br />
- sqlalchemy<br />

Исходный код прилагается.<br />

Визуализация данных приемника системы реализована с помощью отчета Power Bi:
![Pwbi](https://github.com/Yulian771/rbt/raw/main/Pwbi.png)<br />

## Подтверждение результата. Настройка и запуск.<br />
В рамках проведения нефункционального тестирования выявлено, что система осуществляет сбор необходимых данных, доставку данных в приемник, отправку уведомлений в Telegram.
Перед использованием системы необходимо внести изменения в файл Get_YouTube_Data.py, а именно присвоить значения следующим переменным:
- youtube_access_token (API key зарегистрированного приложения для использования YouTube Data API v3)
- channel_id (id YouTube канала с которого будут собираться данные о видео)
- conn_id (Conn Id соответсвующего подключения Airflow)
- table (имя таблицы приемника в БД MS SQL SERVER)
- schema (имя схемы приемника в БД MS SQL SERVER)
- bot_token (токен бота, который используется для уведомлений)
- chat_token (токен чата с ботом, который используется для уведомлений)<br />

После того, как значения для указанных выше переменных определены. Файл Get_YouTube_Data.py и папку func вместе с файлом func.py необходимо поместить в директорию /dags запущенного оркестратора Airflow/

