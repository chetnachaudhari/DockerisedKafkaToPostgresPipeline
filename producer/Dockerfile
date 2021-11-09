FROM python:3.9-slim

WORKDIR /usr/app

COPY ./requirements.txt /usr/app/

RUN pip install -r requirements.txt

COPY . /usr/app

CMD ["python", "order_producer.py"]