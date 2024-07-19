FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY . /app
WORKDIR /app

RUN chmod 0700 entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
