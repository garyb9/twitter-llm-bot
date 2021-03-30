from django.contrib import admin
from django.utils.translation import gettext as _
from .models import TokenURI

class TokenURIAdmin(admin.ModelAdmin):
    """TokenURI model admin"""
    
    ordering = ['id']
    list_display = ['id', 'address',]
    readonly_fields = ['id',]
    fieldsets = (
        (_('Base Info'), {'fields': ('id',)}),
        (_('Address Info'), {'fields': ('address',)}),
        (_('TokenURI Info'),{'fields': ('name', 'description', 'imageURL', 'traits',)}),
    )


admin.site.register(TokenURI, TokenURIAdmin)