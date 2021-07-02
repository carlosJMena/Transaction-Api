FROM python:3.8.2

ENV PYTHONUNBUFFERED 1

COPY belvoapp /belvoapp

WORKDIR /belvoapp

RUN pip install -r requirements.txt

VOLUME /belvoapp

EXPOSE 8080

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
