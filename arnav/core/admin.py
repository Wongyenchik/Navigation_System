from django.contrib import admin
from core.models import User,Product,Map,ProductList,ProductListItem
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','account_type']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name','product_category','stock','location','image']

class MapAdmin(admin.ModelAdmin):
    list_display = ['depart','destination','map']

class ProductListAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'time']

class ProductListItemAdmin(admin.ModelAdmin):
    list_display = ['order','product_id','product_name','product_category', 'stock']

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(ProductList, ProductListAdmin)
admin.site.register(ProductListItem, ProductListItemAdmin)



