FROM python:3

WORKDIR /instance-app

COPY ./instance-app /instance-app
ADD ./utils /instance-app/utils

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "placeholder.py"]