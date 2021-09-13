FROM python:3
workdir /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD [ "python3", "manage.py","runserver" , "0.0.0.0:8000" ]
