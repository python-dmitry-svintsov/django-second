from it_shop.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order_id}'
    message = f'Уважаемый {order.first_name},\n\nВаш заказ обработан.\
                Номер вашего заказа: {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'from: sda6@it_shop.com',
                          [order.email])
    return mail_sent