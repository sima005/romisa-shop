from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, ContactMessage, Order, OrderItem, Product, ProductVariant


def home(request):
    products = list(
        Product.objects.filter(active=True, featured=True)
        .prefetch_related('variants')[:4]
    )
    if not products:
        products = list(Product.objects.filter(active=True).prefetch_related('variants')[:4])

    categories = []
    for category in Category.objects.filter(active=True)[:4]:
        category_product = (
            Product.objects.filter(active=True, category=category)
            .exclude(image='')
            .first()
        )
        categories.append({'category': category, 'product': category_product})

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
    })


def shop(request):
    products = Product.objects.filter(active=True).select_related('category').prefetch_related('variants')
    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(name__icontains=q)
    return render(request, 'store/shop.html', {
        'products': products,
        'categories': Category.objects.filter(active=True),
        'selected': category,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('variants'),
        slug=slug,
        active=True,
    )
    return render(request, 'store/product.html', {'product': product})


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            contact=request.POST.get('contact', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'پیام شما با موفقیت ارسال شد.')
        return redirect('contact')
    return render(request, 'store/contact.html')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    variant_id = request.POST.get('variant_id')
    variant = ProductVariant.objects.filter(
        id=variant_id, product=product, active=True
    ).first() if variant_id else None
    key = f'{product.id}:{variant.id if variant else 0}'
    cart = request.session.get('cart', {})
    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {
            'product_id': product.id,
            'variant_id': variant.id if variant else None,
            'qty': 1,
        }
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, 'محصول به سبد خرید اضافه شد.')
    return redirect(request.POST.get('next') or 'cart')


def remove_from_cart(request, key):
    cart = request.session.get('cart', {})
    cart.pop(key, None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def cart(request):
    cart_data = []
    total = 0
    for key, item in request.session.get('cart', {}).items():
        product = Product.objects.filter(id=item['product_id'], active=True).first()
        if not product:
            continue
        variant = ProductVariant.objects.filter(
            id=item.get('variant_id'), product=product
        ).first() if item.get('variant_id') else None
        price = variant.price if variant else product.final_price
        subtotal = price * item['qty']
        total += subtotal
        cart_data.append({
            'key': key,
            'product': product,
            'variant': variant,
            'qty': item['qty'],
            'price': price,
            'subtotal': subtotal,
        })
    return render(request, 'store/cart.html', {'items': cart_data, 'total': total})


@transaction.atomic
def checkout(request):
    items = []
    total = 0
    for key, item in request.session.get('cart', {}).items():
        product = Product.objects.filter(id=item['product_id'], active=True).first()
        if not product:
            continue
        variant = ProductVariant.objects.filter(
            id=item.get('variant_id'), product=product, active=True
        ).first() if item.get('variant_id') else None
        price = variant.price if variant else product.final_price
        total += price * item['qty']
        items.append((product, variant, item['qty'], price))
    if request.method == 'POST' and items:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            total=total,
        )
        for product, variant, qty, price in items:
            OrderItem.objects.create(
                order=order, product=product, variant=variant,
                quantity=qty, unit_price=price,
            )
        request.session['cart'] = {}
        request.session.modified = True
        return render(request, 'store/success.html', {'order': order})
    return render(request, 'store/checkout.html', {'items': items, 'total': total})
