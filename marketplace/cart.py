from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import NFT


CART_SESSION_ID = 'cart'


def clear_cart(request):
    request.session[CART_SESSION_ID] = {}
    request.session.modified = True
    return redirect('cart_detail')


def update_cart(request, nft_id):
    cart = _get_cart(request)
    str_id = str(nft_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart[str_id] = qty
    else:
        cart.pop(str_id, None)
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True
    return redirect('cart_detail')



def _get_cart(request):
    return request.session.setdefault(CART_SESSION_ID, {})

def add_to_cart(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    cart = _get_cart(request)
    str_id = str(nft_id)
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        cart[str_id] = {
            'quantity': 1,
            'price': float(nft.price),
            'title': nft.title,
        }
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', reverse('nft_list')))

def remove_from_cart(request, nft_id):
    cart = _get_cart(request)
    str_id = str(nft_id)
    if str_id in cart:
        if cart[str_id]['quantity'] > 1:
            cart[str_id]['quantity'] -= 1
        else:
            del cart[str_id]
        request.session[CART_SESSION_ID] = cart
        request.session.modified = True
    return redirect('cart_detail')

def cart_detail(request):
    cart = _get_cart(request)
    nft_ids = cart.keys()
    nfts = NFT.objects.filter(id__in=nft_ids)
    cart_items = []
    total_price = 0
    total_quantity = 0
    for nft in nfts:
        item = cart.get(str(nft.id), {})
        qty = item.get('quantity', 0)
        subtotal = nft.price * qty
        total_price += subtotal
        total_quantity += qty
        cart_items.append({
            'nft': nft,
            'quantity': qty,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_count': len(cart_items),
        'cart': cart,
        'nfts': nfts,
        'default': 'cart_detail',
        'title': 'Cart',
        'description': 'Cart',
        'keywords': 'Cart',
        'author': 'Amirhossein',
        'url': 'https://SormatSea.io/cart/',
        'image': 'https://SormatSea.io/static/images/logo.png',
    }
    return render(request, 'marketplace/cart_detail.html', context)
# Additional features
def update_cart_quantity(request, nft_id):
    cart = _get_cart(request)
    str_id = str(nft_id)
    qty = int(request.POST.get('quantity', 1))
    if str_id in cart:
        if qty > 0:
            cart[str_id]['quantity'] = qty
        else:
            del cart[str_id]
        request.session[CART_SESSION_ID] = cart
        request.session.modified = True
    return redirect('cart_detail')

def empty_cart(request):
    request.session[CART_SESSION_ID] = {}
    request.session.modified = True
    return redirect('cart_detail')

def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('cart_detail')
    # Here you would handle payment and NFT transfer logic
    # For now, just clear the cart and show a success page
    request.session[CART_SESSION_ID] = {}
    request.session.modified = True
    return render(request, 'marketplace/checkout_success.html')
