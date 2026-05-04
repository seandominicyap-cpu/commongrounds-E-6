from django.db.models.signals import post_save
from django.dispatch import receiver
from merchstore.models import Transaction


@receiver(post_save, sender=Transaction)
def update_stock_and_status(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock = max(0, product.stock - instance.amount)
        if product.stock == 0:
            product.status = "Out of stock"
        elif product.status == "Out of stock" and product.stock > 0:
            product.status = "Available"
        product.save()
