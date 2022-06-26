from django.test import TestCase
from django.utils import timezone
from ..models import *
import ads.tests.test_models as ad_test

def modelInst():

    Order.objects.create(
        first_name = 'Test',
        last_name ='UserOne',
        email = 'testuser1@example.com',
        postal_code = 'TYT 4GT',
        address ='39st 67ave',
        city = "California",
        created = timezone.now(),
        updated = timezone.now(),
        paid= False
    )

    order_item1 = {
        'order' :Order.objects.get(pk=1),
        'ad' : Ad.objects.get(pk=1),
        'price' :4.99,
        'quantity': 1
    }
    OrderItem.objects.create(
        order = order_item1['order'],
        ad = order_item1['ad'],
        price = order_item1['price'],
        quantity =order_item1['quantity']
    )
    pass
class TestOrderModel(TestCase):
    def setUp(self):
        ad_test.modelInst()
        modelInst()
        pass
    def test_str(self):
        order = Order.objects.get(pk=1)
        t = f"Order: No.1, by Test UserOne (testuser1@example.com), placed on {order.created} |  1 total items | total:$4.99 | address 39st 67ave TYT 4GT California | paid False"
        self.assertEqual(str(order),t)
    pass
class TestOrderItemModel(TestCase):
    def setUp(self):
        ad_test.modelInst()
        modelInst()
        pass
    def test_str(self):
        ord_item = OrderItem.objects.get(pk=1)
        ad = Ad.objects.get(pk=1)
        t = f'Order (1): {ad.title}, 1 item(s). ${4.99}'
        self.assertEqual(str(ord_item),t)
