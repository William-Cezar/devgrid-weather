FROM python:3.9-buster
WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libevent-dev python3-dev  

COPY requirements.txt /app/.
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . /app
RUN python manage.py makemigrations && python manage.py migrate
EXPOSE 8007
CMD ["gunicorn", "open_weather_project.wsgi:application", "-k", "gevent", "-b", "0.0.0.0:8007"]
