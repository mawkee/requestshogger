FROM python:3.7-alpine

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD hogger .

CMD ["python", "reqhogger.py"]
