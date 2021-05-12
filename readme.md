## Zorro Framework

Проект включает в себя директорию с шаблонами **templates** и директорию с самим фреймворком **Zorro Framework**. 
Остальная логика прописана в файлах urls.py и views.py 
Запустить проект можно с помощью runner.py. 

`python runner.py [-p Port]`

При запуске можно добавить дополнительный параметр `-p` через который задаётся порт, на котором будет работать приложение.

Проект можно запускать и через uwsgi. Например, из WSL можно запустить следующим образом:

`uwsgi --http-socket :8888 --binary-path <path to wsgi library> --plugin python3 --wsgi-file <path to project>/runner.py`

UPD:

В проект добавлены два новых вида wsgi-application: LoggingApplication и FakeApplication. Теперь при запуске приложения
можно выбрать какой wsgi-application запускать следующим образом:

`python runner.py [-p Port] [-a Application]`

По умолчанию запускается Framework application. LoggingApplication запускается через параметр `[-a log_app]`, 
а FakeApplication через параметр `[-a fake_app]`. Для помощи в запуске приложения можно использовать параметр -h

`python runner.py -h`