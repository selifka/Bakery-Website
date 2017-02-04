from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
def about(request):
    return render(request, 'shop/about.html', {})

def home(request):
    return render(request, 'shop/home.html', {})

def contact(request):
    return render(request, 'shop/contact.html', {})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    stock_number = list(range(product.stock))
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,'cart_product_form': cart_product_form,'stock_number': stock_number})