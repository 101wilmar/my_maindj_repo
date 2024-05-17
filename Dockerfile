#образ для сбора контейнера
FROM python:3.12.2

#рабочая папка проекта 
WORKDIR /app

#копируем ключ и выставляем зависимости 
COPY cert.crt /app
COPY ./requirements.txt /app

#обновление и установка необходимых пакетов
RUN apt-get update -y && \
    apt-get install -y \
    openssl
RUN pip install django-extensions

# Копируем файл db.json
COPY db.json /app
# Устанавливаем зависимости Python из requirements.txt
RUN pip install -r requirements.txt

# Копируем все остальные файлы 
COPY . .
EXPOSE 8000
ENV PYTHONIOENCODING=utf-8
# Запускаем Django приложение
CMD python /app/manage.py migrate && python /app/manage.py loaddata db.json && python /app/manage.py runserver_plus --cert-file cert.crt 0.0.0.0:8000