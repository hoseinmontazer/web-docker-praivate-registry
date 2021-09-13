FROM python:3
workdir /app
COPY app .
RUN pip install -r requirements.txt
CMD [ "python3", "manage.py","runserver" , "0.0.0.0:8000" ]

