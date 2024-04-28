FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 26601

ENTRYPOINT [ "python" ]
CMD ["main.py" ]