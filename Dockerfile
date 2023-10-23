FROM python:3
MAINTAINER nithinhemachandran@gmail.com
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./hello.py" ]
