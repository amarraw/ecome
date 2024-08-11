from django.contrib import admin
from ecomeapp.models import Contact , Product 
from order.models import Order
# Register your models here.

admin.site.register(Contact)
admin.site.register(Order)



class ProductAdmin(admin.ModelAdmin):
    list_filter=('category',)
    search_fields = ('product_name','category',)


admin.site.register(Product, ProductAdmin)





