from django.contrib import admin
from .models import NFT, Category, Transaction
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


class NFTAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "id", "price_irt", "price_polygon", "category", "blockchain")
    list_filter = ("category", "blockchain")
    search_fields = ("name", "description")

    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Details', {
            'fields': ('category', 'owner', 'price', 'blockchain', 'created_at')
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


admin.site.register(NFT, NFTAdmin)
admin.site.register(Category, CategoryAdmin)
