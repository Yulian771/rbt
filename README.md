# rbt

Get_YouTube_Data.py и func - DAG <br />
YouTube Report.pbix - файл отчета <br />


Документация<br />

Требования<br />
Система должна осуществлять сбор данных о видеороликах опубликованных на платформе YouTube<br />
за последние 24 часа с использованием YouTube Data API. Данные должны включать: название видео,<br />
количество просмотров, количество лайков, количество комментариев.<br />

Ежедневно отправлять уведомление в Telegram с информацией о топ-5 видеороликах с названием,<br />
количеством просмотров, лайков, комментариев и ссылкой на видео.<br />

Система включает в себя отчет PWBI с визуализацией графиков изменения количества просмотров,<br />
лайков и комментариев во времени.<br />

Реализация<br />
Процесс загрузки данных из источника YouTube Data API в приемник разрабатываемой системы<br />
реализован с помощью DAG-оркестратора Airflow на языке программирования Python.<br />
DAG содержит задачи на соответствующий запрос данных из источника YouTube Data API.<br />
Обработку полученных данных, отправку очищенных данных в приемник, а так же отправку уведомления в Telegram.<br />
Для реализации этого процесса были использованы следующие библиотеки Python:<br />
  requests<br />
  pandas<br />
  sqlalchemy<br />
  <br />
Исходный код прилагается.<br />
