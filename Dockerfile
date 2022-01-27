FROM python:3.10.2-slim-buster

WORKDIR /code

COPY code/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /code .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]