from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

from django.views.generic.edit import FormView

class OrderFormView(FormView):
    form_class = OrderCreateForm
    template_name = 'orders/order_form.html'
    success_url = 'orders/order_confirm.html'
    def post(self,request,*args,**kwargs):
        form = OrderCreateForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        ad=item['ad'],
                                        price=item['price'],
                                        quantity=1)
            # clear the cart
            cart.clear()
            cart.clear()
            return render(request,
                          'orders/order_confirm.html',
                          {'order': order})
        else:
            form = OrderCreateForm()
        return render(request,
                      'orders/order_confirm.html',
                      {'cart': cart, 'form': form})
