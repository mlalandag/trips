FROM python:3.8

COPY requirements.txt /tmp/

RUN python3 -m pip install -r /tmp/requirements.txt

COPY app.py /opt/

WORKDIR /opt/

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]