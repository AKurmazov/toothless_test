from django.shortcuts import render, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import JsonResponse

from items.models import Item

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', context={'items': items})


def thanks(request):
    return render(request, 'items/thanks.html')


def item_details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'items/item_details.html', context=context)


def buy_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"Error": "Not found.",})

    product_data = {
        'name': item.name,
    }
    if item.description:
        product_data['description'] = item.description

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item.price * 100),
                    'product_data': product_data,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')),
        cancel_url=request.build_absolute_uri(reverse('index')),
    )

    return JsonResponse({'session_id': session.id})