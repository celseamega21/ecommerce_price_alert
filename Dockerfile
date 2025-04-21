FROM python:3.10

WORKDIR /scrapping_ecommerce

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["gunicorn", "scrapping_ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]