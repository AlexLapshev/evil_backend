FROM python:3.8.2-slim

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 1984

CMD /bin/bash

CMD python -m api.main
