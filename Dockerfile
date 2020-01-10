FROM python:3.7-alpine

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD hogger .

# Don't bind to a specific address
ENV HOGGER_HOST="0.0.0.0"
ENTRYPOINT ["python", "reqhogger.py"]

EXPOSE 8910
