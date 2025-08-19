FROM python:3.9-slim

COPY handlers.py requirements.txt /src/

WORKDIR /src/

RUN pip3 install -r requirements.txt

CMD kopf run handlers.py --verbose