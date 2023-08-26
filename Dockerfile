FROM python:3.9

WORKDIR /app
COPY . /app

RUN apt-get update

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["python", "-u", "main.py"]