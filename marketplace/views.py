from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from django.views.decorators.http import require_GET 
from django.utils import timezone
from django.db.models import F, Count, ExpressionWrapper, DurationField
from django.views import View

from .models import NFT, Category, Subcategory, Transaction
from .forms import RegisterForm, NFTForm
from .cart import cart_detail, add_to_cart, remove_from_cart



def ton_nft_collection(request):
    # Get some NFTs for demonstration
    nfts = NFT.objects.all()[:8]  # Get 8 NFTs for demo
    
    # Add mock TON prices for demonstration
    for nft in nfts:
        nft.ton_price = round(float(nft.price) * 0.00025, 2)  # Mock conversion
    return render(request, 'marketplace/ton_nft_collection.html', {'nfts': nfts})


def wallet_connect(request):
    return render(request, 'marketplace/wallet_connect.html')

def nft_create(request):
    if request.method == 'POST':
        form = NFTForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('marketplace:nft_list')
    else:
        form = NFTForm()
    return render(request, 'nft_create.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('marketplace:nft_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def create_nft(request):
    if request.method == 'POST':
        form = NFTForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('nft_list')
    else:
        form = NFTForm()
    return render(request, 'create_nft.html', {'form': form})

class ProductView(View):
    def get(self, request, subcategory_id=None):
        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
            products = subcategory.item.all()
            return render(request, 'products.html', {'subcategory_list': products})
        else:
            category_list = Category.objects.all()
            return render(request, 'products.html', {'category_list': category_list})

@require_GET
def home(request):
    now = timezone.now()
    
    # Featured NFTs
    featured_qs = NFT.objects.filter(
        is_featured=True,
        featured_until__gte=now
    ).order_by('-created_at')

    featured_qs = featured_qs.annotate(
        time_left=ExpressionWrapper(
            F('featured_until') - now,
            output_field=DurationField()
        )
    )
    featured_nfts = featured_qs[:10]
    total_featured = featured_qs.count()

    # Trending NFTs
    trending_nfts = NFT.objects.order_by('-views')[:5]

    # Top categories
    top_categories = (
        Category.objects
        .annotate(num_nfts=Count('nft'))
        .order_by('-num_nfts')[:5]
    )

    # Recommended NFTs
    recommended_nfts = None
    if request.user.is_authenticated:
        # Simple recommendation logic - modify as needed
        recommended_nfts = NFT.objects.order_by('-created_at')[:5]

    context = {
        'featured_nfts': featured_nfts,
        'total_featured': total_featured,
        'trending_nfts': trending_nfts,
        'top_categories': top_categories,
        'recommended_nfts': recommended_nfts,
    }
    return render(request, 'home.html', context)

# Add these missing views that are referenced in your URLs
def nft_list(request):
    nfts = NFT.objects.all()
    return render(request, 'marketplace/nft_list.html', {'nfts': nfts})

def nft_detail(request, slug):
    nft = get_object_or_404(NFT, slug=slug)
    return render(request, 'marketplace/nft_detail.html', {'nft': nft})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'marketplace/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    nfts = category.nft_set.all()
    return render(request, 'marketplace/category_detail.html', {'category': category, 'nfts': nfts})

def nfts_view(request):
    nfts = NFT.objects.all()
    return render(request, 'marketplace/nfts.html', {'nfts': nfts})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('nft_list')
    else:
        form = RegisterForm()
    return render(request, 'marketplace/register.html', {'form': form})

@login_required
def initiate_payment(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    if request.method == 'POST':
        from .payment_nft import NFTPaymentManager
        payment_manager = NFTPaymentManager()
        result = payment_manager.process_payment(nft_id, request.user.id)
        if result['success']:
            return redirect(result['payment_url'])
        else:
            messages.error(request, f"Payment failed: {result['message']}")
            return redirect('nft_detail', slug=nft.slug)
    return render(request, 'marketplace/payment_initiate.html', {'nft': nft})

def payment_verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    
    if status == 'OK' and authority:
        try:
            from .payment_nft import NFTPaymentManager
            transaction = Transaction.objects.get(bank_reference=authority)
            payment_manager = NFTPaymentManager()
            result = payment_manager.verify_payment(authority, transaction.amount)
            
            if result['success']:
                messages.success(request, "Payment successful!")
                return redirect('nft_detail', slug=result['nft'].slug)
            else:
                messages.error(request, f"Payment failed: {result['message']}")
        except Transaction.DoesNotExist:
            messages.error(request, "Transaction not found")
    else:
        messages.warning(request, "Payment was canceled")
    
    return redirect('nft_list')