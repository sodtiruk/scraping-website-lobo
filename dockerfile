FROM python:3.10.13

RUN mkdir -p /src/app

WORKDIR /src/app

COPY ./requirements.txt ./
COPY ./main.py ./

RUN pip install -r requirements.txt

CMD [ "python", "main.py"]









