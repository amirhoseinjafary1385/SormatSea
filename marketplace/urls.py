from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import cart
from .views import ProductView


app_name = 'marketplace'  # Add this line to enable URL namespacing

urlpatterns = [
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='marketplace/password_reset.html'),
         name='password_reset'),
    path('ton-nft/', views.ton_nft_collection, name='ton_nft_collection'),
    # Wallet connection
    path('wallet/connect/', views.wallet_connect, name='wallet_connect'),
    
    # NFT creation (choose one, not both)
    path('nft/create/', views.nft_create, name='nft_create'),
    # path('create-nft/', views.create_nft, name='create_nft'),  # Remove this duplicate
    
    # Products
    path('products/', ProductView.as_view(), name='product-list'),
    path('products/<int:subcategory_id>/', ProductView.as_view(), name='product-by-subcategory'),
    
    # Cart
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:nft_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:nft_id>/", views.remove_from_cart, name="remove_from_cart"),
    
    # Home / NFT list
    path("", views.nft_list, name="nft_list"),
    
    # Alternative "all NFTs" page
    path("nfts/", views.nfts_view, name="nfts"),
    
    # Single-NFT detail by slug
    path("nft/<slug:slug>/", views.nft_detail, name="nft_detail"),
    
    # Category listing & detail
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),  # Changed to int
    
    # User registration and authentication
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name='marketplace/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='marketplace:nft_list'), name="logout"),
    
    # Payment flow
    path("payment/initiate/<int:nft_id>/", views.initiate_payment, name="initiate_payment"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),  # Fixed function name
]

