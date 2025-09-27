
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('accounts/', include('allauth.urls')),
    path('', include('marketplace.urls')),  

    path('accounts/', include('django.contrib.auth.urls')),  

   
    path('login/', auth_views.LoginView.as_view(
        template_name='marketplace/login.html',
        redirect_authenticated_user=True,
        next_page='nft_list',
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
