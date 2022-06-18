FROM python:latest

WORKDIR /var/www
USER app

COPY update-ddns.sh .
COPY passwd .
COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "uvicorn",  "main:app", "--port", "8000" ]