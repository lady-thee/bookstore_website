FROM python:3.11

ENV VAR1=10

ENV PYTHONDONTWRITEBYTECODE=1 

ENV PYTHONUNBUFFERED=1 

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip 
RUN pip install pipenv && pipenv install --dev --system --deploy 

WORKDIR /app/bookstore_app 
COPY . /app 

EXPOSE 8000 

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

