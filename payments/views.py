import stripe
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, Discount, Tax

def get_stripe_key(currency):
    if currency == 'eur':
        return settings.STRIPE_SECRET_KEY_EUR, settings.STRIPE_PUBLIC_KEY_EUR
    return settings.STRIPE_SECRET_KEY_USD, settings.STRIPE_PUBLIC_KEY_USD

def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    stripe.api_key, stripe_public_key = get_stripe_key(item.currency)

    try:
        # Создаём заказ для одиночного товара
        order = Order.objects.create()
        order.items.add(item)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{request.scheme}://{request.get_host()}/success/?order_id={order.id}',
            cancel_url=f'{request.scheme}://{request.get_host()}/cancel/',
            metadata={'order_id': order.id},
        )
        return JsonResponse({'sessionId': session.id, 'publicKey': stripe_public_key})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def buy_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    stripe.api_key, stripe_public_key = get_stripe_key(order.get_currency())

    try:
        line_items = [{
            'price_data': {
                'currency': order.get_currency(),
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        } for item in order.items.all()]

        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': f'{request.scheme}://{request.get_host()}/success/?order_id={order.id}',
            'cancel_url': f'{request.scheme}://{request.get_host()}/cancel/',
            'metadata': {'order_id': order.id},
        }

        if order.discount and order.discount.stripe_coupon_id:
            session_params['discounts'] = [{'coupon': order.discount.stripe_coupon_id}]
        if order.tax and order.tax.stripe_tax_rate_id:
            session_params['automatic_tax'] = {'enabled': False}
            session_params['line_items'][0]['tax_rates'] = [order.tax.stripe_tax_rate_id]

        session = stripe.checkout.Session.create(**session_params)
        return JsonResponse({'sessionId': session.id, 'publicKey': stripe_public_key})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    orders = Order.objects.all()  # Передаём список заказов для выбора
    _, stripe_public_key = get_stripe_key(item.currency)
    return render(request, 'payments/item_detail.html', {'item': item, 'stripe_public_key': stripe_public_key, 'orders': orders})

def add_to_order(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        order_id = request.POST.get('order_id')
        if order_id == 'new':
            order = Order.objects.create()
        else:
            order = get_object_or_404(Order, id=order_id)
        order.items.add(item)
        order.save()
        return redirect('order_detail', order_id=order.id)
    return redirect('item_detail', item_id=item_id)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    _, stripe_public_key = get_stripe_key(order.get_currency())
    return render(request, 'payments/order_detail.html', {'order': order, 'stripe_public_key': stripe_public_key})

def home(request):
    try:
        items = Item.objects.all()
        orders = Order.objects.all()
    except Exception as e:
        items = []
        orders = []
        print(f"Error: {e}")
    return render(request, 'payments/home.html', {'items': items, 'orders': orders})

def payment_success(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id) if order_id else None
    return render(request, 'payments/success.html', {'order': order})

def payment_cancel(request):
    return render(request, 'payments/cancel.html')