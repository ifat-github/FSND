FROM python:stretch

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt


ENTRYPOINT ["gunicorn", "-b", ":5000", "main:APP"]
