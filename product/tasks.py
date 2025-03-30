from celery import shared_task
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.utils.html import escape
from .scrape import Scrape
from .models import PriceHistory, Product
from .scrape import clean_price

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def check_price(self):
    """Check product prices periodically and send an email when the product price is dropped."""

    products = Product.objects.all()

    for product in products:
        scraper = Scrape(product.name).scrape_tokped()
        if not scraper:
            logger.warning(f"Failed to scrape price for {product.name}")
            continue

        new_price = scraper.get("discount_price")
        
        if clean_price(new_price) < clean_price(product.last_price):
            product_name_escape = escape(product.name)

            body_html = f"""
            <html>
            <body>
                <h2>Hurry! The product you're tracking has dropped in price!</h2>
                <p>Hello, {product.email}</p>
                <p>The price of <strong>{product_name_escape}</strong> has dropped, and we thought you'd love to know!</p>

                <p><strong>Previous Price: </strong><s>{product.last_price}</s></p>
                <p><strong>Current Price: </strong>{new_price}</p>
            
                <p>
                    <a href="{product.url}">
                    Check it now! 🔎
                    </a>
                </p>
            </body>
            </html>
            """

            try:
                send_mail(
                    f"Price Drop Alert!!!",
                    "",
                    None,
                    [product.email],
                    fail_silently=False,
                    html_message=body_html
                )
                logger.info(f"Email successfully sent to {product.email}")
            except Exception as e:
                logger.error(f"Failed to send email to {product.email}: {e}")
                raise self.retry(exc=e)
    
            # save new price to database
            PriceHistory.objects.create(product=product, price=new_price)
            product.last_price = new_price
            product.save()