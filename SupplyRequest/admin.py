from MakerBarManager.SupplyRequest.models import Supplier, Product, Order_Request,Shipment
from django.contrib import admin

#class ProductAdmin(admin.ModelAdmin):
#    list_display = ('id','order','shipment','supplier','name','part_number','quantity','cost')

class OR_ProductInline(admin.TabularInline):
    model = Product
    #exclude = ('shipment',)
    extra = 5

class Order_RequestAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Request Information' , {'fields': ['requestor','request_date','request_placed']}),
    ]
    inlines = [OR_ProductInline]
    list_display = ('id','request_date','request_placed')
    list_filter = ['request_date']

class ShipmentAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    ('Shipment Information' , {'fields': ['supplier','order_date','shipper','tracking_number','status']}),
    #]
    list_display = ('id','order_date','shipper','tracking_number','status')



admin.site.register(Supplier)
admin.site.register(Shipment,ShipmentAdmin)
#admin.site.register(Product,ProductAdmin)
admin.site.register(Order_Request,Order_RequestAdmin)
