1. Скачать репозиторий из ГИТ на удаленный сервер. (git clone https://github.com/Danil026/depl_auto.git)
2. Создать/Развернуть базу данных. (https://www.postgresql.org/download/)
3. Скачать Python3 (https://www.python.org/downloads/)
4. Импортировать все библиотеки из файла requirements.txt(pip install -r "C:\Users\User\PycharmProjects\venvAutodep\venv\Автодепл\requirements.txt")
5. Исправить файл config.ini указать(свои данные для подключения к БД [db_data] и расположения целевых папок [path_data] ) 
6. Автоматизировать скрипт при помощи cron или Планировщик задач.(AutoAndDeploy.py -код для симулирования работы кассовых аппаратов,Writedb.py - код для записи данных в Базу данных, и перемещенниея обработанных файлов папку Архив)
Примечание. DB_singleton.py код с Классом Singleton  для подключения к БД. При запуске Writedb.py через планировщик задач Windows, в файле сценариев(.bat)для корректной работы,также необходимо его указывать.Пример файл Writedb.bat
