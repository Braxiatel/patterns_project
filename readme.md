## Zorro Framework

Проект включает в себя директорию с шаблонами **templates** и директорию с самим фреймворком **Zorro Framework**. 
Остальная логика прописана в файлах urls.py и views.py 
Запустить проект можно с помощью runner.py. 

`python runner.py [-p Port]`

При запуске можно добавить дополнительный параметр `-p` через который задаётся порт, на котором будет работать приложение.

Проект можно запускать и через uwsgi. Например, из WSL можно запустить следующим образом:

`uwsgi --http-socket :8888 --binary-path <path to wsgi library> --plugin python3 --wsgi-file <path to project>/runner.py`
