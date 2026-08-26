from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from . import cart
from .views import ProductView

app_name = 'marketplace'

urlpatterns = [
    # ============================================
    # HOME & LANDING
    # ============================================
    path("", views.nft_list, name="nft_list"),
    path("nfts/", views.nfts_view, name="nfts"),
    
    # ============================================
    # AUTHENTICATION
    # ============================================
    # Registration
    path("register/", views.register_view, name="register"),
    
    # Login/Logout
    path("login/", auth_views.LoginView.as_view(
        template_name='marketplace/login.html',
        redirect_authenticated_user=True
    ), name="login"),
    
    path("logout/", auth_views.LogoutView.as_view(
        next_page='marketplace:nft_list'
    ), name="logout"),
    
    # ============================================
    # PASSWORD RESET - COMPLETE FLOW
    # ============================================
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='marketplace/password_reset.html',
             email_template_name='marketplace/password_reset_email.html',
             subject_template_name='marketplace/password_reset_subject.txt',
             success_url='done/'
         ),
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='marketplace/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='marketplace/password_reset_confirm.html',
             success_url='../complete/'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='marketplace/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # ============================================
    # NFT MANAGEMENT
    # ============================================
    # NFT List & Detail
    path("nft/<slug:slug>/", views.nft_detail, name="nft_detail"),
    path("nft/create/", views.nft_create, name="nft_create"),
    path("nft/<slug:slug>/edit/", views.nft_edit, name="nft_edit"),
    path("nft/<slug:slug>/delete/", views.nft_delete, name="nft_delete"),
    path("nft/<slug:slug>/purchase/", views.nft_purchase, name="nft_purchase"),
    
    # Featured NFTs
    path("nfts/featured/", views.nft_featured, name="nft_featured"),
    path("nfts/new/", views.nft_new, name="nft_new"),
    path("nfts/trending/", views.nft_trending, name="nft_trending"),
    
    # ============================================
    # CATEGORIES
    # ============================================
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail_by_slug, name="category_detail_by_slug"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("subcategory/<slug:slug>/", views.subcategory_detail, name="subcategory_detail"),
    
    # ============================================
    # SHOPPING CART
    # ============================================
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:nft_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:nft_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:nft_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("cart/checkout/", views.cart_checkout, name="cart_checkout"),
    
    # ============================================
    # CHECKOUT & PAYMENT
    # ============================================
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
    
    # Payment Flow
    path("payment/initiate/<int:nft_id>/", views.initiate_payment, name="initiate_payment"),
    path("payment/initiate/cart/", views.initiate_cart_payment, name="initiate_cart_payment"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),
    path("payment/webhook/", views.payment_webhook, name="payment_webhook"),
    path("payment/apply-coupon/", views.apply_coupon, name="apply_coupon"),
    
    # ============================================
    # WALLET & BLOCKCHAIN
    # ============================================
    path("wallet/connect/", views.wallet_connect, name="wallet_connect"),
    path("wallet/disconnect/", views.wallet_disconnect, name="wallet_disconnect"),
    path("wallet/status/", views.wallet_status, name="wallet_status"),
    path("ton-nft/", views.ton_nft_collection, name="ton_nft_collection"),
    
    # ============================================
    # USER PROFILE
    # ============================================
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/nfts/", views.my_nfts, name="my_nfts"),
    path("profile/purchases/", views.my_purchases, name="my_purchases"),
    path("profile/sales/", views.my_sales, name="my_sales"),
    path("profile/favorites/", views.my_favorites, name="my_favorites"),
    path("profile/wallet/", views.profile_wallet, name="profile_wallet"),
    path("profile/notifications/", views.notifications, name="notifications"),
    
    # ============================================
    # USER INTERACTIONS
    # ============================================
    path("nft/<slug:slug>/like/", views.nft_like, name="nft_like"),
    path("nft/<slug:slug>/favorite/", views.nft_favorite, name="nft_favorite"),
    path("nft/<slug:slug>/review/", views.nft_review, name="nft_review"),
    path("nft/<slug:slug>/share/", views.nft_share, name="nft_share"),
    
    # ============================================
    # PRODUCTS (Legacy)
    # ============================================
    path('products/', ProductView.as_view(), name='product-list'),
    path('products/<int:subcategory_id>/', ProductView.as_view(), name='product-by-subcategory'),
    
    # ============================================
    # SEARCH
    # ============================================
    path("search/", views.search_view, name="search"),
    
    # ============================================
    # STATIC PAGES
    # ============================================
    path("about/", TemplateView.as_view(template_name="marketplace/about.html"), name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("faq/", TemplateView.as_view(template_name="marketplace/faq.html"), name="faq"),
    path("terms/", TemplateView.as_view(template_name="marketplace/terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="marketplace/privacy.html"), name="privacy"),
    
    # ============================================
    # API (Optional - If you're building an API)
    # ============================================
    # path("api/", include("api.urls")),
]