FROM python:3-alpine3.10
WORKDIR /athursto-app
COPY . /athursto-app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python ./app.py

