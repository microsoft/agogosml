FROM python:3.7-alpine3.8
ADD ./sample-app/webapp/requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt
ADD ./sample-app/webapp /opt/webapp/
ADD ./utils /opt/webapp/utils
WORKDIR /opt/webapp
EXPOSE 5000
CMD ["python", "app.py"]
