from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def on_order_create(sender, **kwargs):
    print("Order created", kwargs['order'])