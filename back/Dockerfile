FROM python:3.11

COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]
EXPOSE 26601
