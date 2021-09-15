From python:3.8

WORKDIR /src
COPY app.py .
COPY words.txt .

CMD [ "python", "app.py" ]