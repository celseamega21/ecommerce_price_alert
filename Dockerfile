FROM python:3.10

WORKDIR /scrapping_ecommerce

COPY requirements.txt .
RUN pip install --no--chace-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "scrapping_ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]