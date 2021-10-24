from decimal import Decimal
from django.conf import settings
from ads.models import Ad

class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart  = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    def add(self,ad):
        ad_id = str(ad.id)
        if ad_id not in self.cart:
            self.cart[ad_id] = {
                'price':str(ad.price)
            }
        self.save()
    def sub(self,ad):
        ad_id = str(ad.id)
        if ad_id in self.cart:
            del self.cart[ad_id]
            self.save()
    def __iter__(self):
        ad_ids = self.cart.keys()
        ads = Ad.objects.filter(id__in=ad_ids)
        cart = self.cart.copy()
        for ad in ads:
            cart[str(ad.id)]['ad'] = ad
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item
    def __len__(self):
        return len(self.cart)
    def get_total_price(self):
        return sum([Decimal(item['price']) for item in self.cart.values()])
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
