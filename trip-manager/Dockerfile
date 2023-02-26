FROM python:3.8

COPY requirements.txt /tmp/

RUN python3 -m pip install -r /tmp/requirements.txt

COPY app.py /opt/

WORKDIR /opt/

CMD ["python3", "app.py"]