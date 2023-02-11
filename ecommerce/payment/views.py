from django.shortcuts import render

from .models import ShippingAddress, OrderItem, Order
from cart.cart import Cart


def checkout(request):
    if request.user.is_authenticated:
        try:
            shippingaddress = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping': shippingaddress}

            return render(request, 'payment/checkout.html', context=context)
        except:
            pass
    return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')

        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + zipcode)

        cart = Cart(request)

        total_cost = cart.get_total()

        '''
            Order variation
            1) Create order -> Accounts users With + Without Ship
            2) Create order -> Guest users without an account
        '''
        if request.user.is_authenticated():
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user,
                )
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                )


def payment_success(request):
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')
