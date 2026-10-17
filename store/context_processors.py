def cart_context(request):
    cart = request.session.get('cart', {})
    return {'cart_count': sum(item.get('qty', 0) for item in cart.values())}
