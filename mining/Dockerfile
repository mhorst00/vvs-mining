FROM python:3.11

WORKDIR /code

RUN mkdir /data

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./*.py ./*.csv /code/

CMD [ "python", "download.py" ]
