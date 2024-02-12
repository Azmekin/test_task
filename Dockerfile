FROM python:3.10

RUN mkdir app
WORKDIR /app/


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget

RUN apt-get install -y python3 python3-pip



RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN ["chmod", "+x", "start.sh"]

ENTRYPOINT ["sh", "start.sh"]