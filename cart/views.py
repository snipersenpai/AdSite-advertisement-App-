from django.shortcuts import render,redirect,get_object_or_404

from django.views.decorators.http import require_POST
from ads.models import Ad
from .cart import Cart
from .forms import CartAddAdForm


@require_POST
def cart_add(request,ad_id):
    cart = Cart(request)
    ad = get_object_or_404(Ad,id=ad_id)
    form = CartAddAdForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(ad)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request,ad_id):
    cart = Cart(request)
    ad = get_object_or_404(Ad,id=ad_id)
    cart.sub(ad)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request,'cart/detail.html',{'cart':cart})
