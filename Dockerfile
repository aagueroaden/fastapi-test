FROM python:3.8-slim

WORKDIR /salesforce_fastapi

COPY requirements.txt /salesforce_fastapi/
RUN pip3 install -r requirements.txt

COPY . /salesforce_fastapi/

EXPOSE 9000

CMD ["python", "main.py"]