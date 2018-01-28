FROM arm32v7/python:3.6-jessie

ENV WORKDIR /data/dht22

COPY ./dht22 /data/dht22

RUN pip install pip --upgrade --force && \
    pip install -r $WORKDIR/requirements.txt

CMD ["sh", "-c", "python $WORKDIR/run.py"]
