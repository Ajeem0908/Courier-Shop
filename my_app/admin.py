from django.contrib import admin
from .models import CourierShops, Customer, Delivery

from django.contrib import admin
from .models import CourierShops

class CourierShopsAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'owner_name', 'city', 'address', 'pincode']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner_name=request.user.username)  
        return qs

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if not request.user.is_superuser and obj.owner_name != request.user.username:
                return False  
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if not request.user.is_superuser and obj.owner_name != request.user.username:
                return False
        return super().has_delete_permission(request, obj)

admin.site.register(CourierShops, CourierShopsAdmin)



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'billing_address', 'pincode', 'created_at', 'updated_at', 'status')
    search_fields = ('customer_name', 'phone_number', 'status')

admin.site.register(Customer, CustomerAdmin)

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'customer_name', 'courier_shop', 'status', 'delivery_date')
    list_filter = ('status', 'delivery_date')
    search_fields = ('tracking_number', 'customer_name', 'courier_shop__shop_name')
    ordering = ['delivery_date']

admin.site.register(Delivery, DeliveryAdmin)

from django.contrib.auth.models import User