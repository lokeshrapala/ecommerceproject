from django.contrib import admin
from .models import Product,Stock
class Productadmin(admin.ModelAdmin):
    list_display = ['pid', 'pname', 'pcat','pcost','pmfdt','pexpdt']
    list_filter = ['pcat','pmfdt','pexpdt']
    class meta:
     model=Product
admin.site.register(Product,Productadmin)
class Stockadmin(admin.ModelAdmin):
    list_display=['prodid','tot_qty','last_update','next_update']
    list_filter=['prodid']
    class meta:
        model=Stock
admin.site.register(Stock,Stockadmin)
