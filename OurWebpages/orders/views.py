from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from shop.models import Product # Connect with shop app's model.
from django.contrib import messages # Import message framework

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])  
            # clear the cart
            update = Product.objects.get(name=item['product'])
            update.stock = update.stock - item['quantity']
            if update.stock >= 0:
                    # updated file will be saved and update on admin page.
                    update.save()
                    # clear the cart
                    cart.clear()
                    return render(request,
                          'orders/order/created.html',
                          {'order': order})
            else:
                    # updated file will not be saved and update on admin page.
                    messages.error(request, 'Error submitting your order. Please change your amount of your order clicking "Your cart:" link.')
                    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})