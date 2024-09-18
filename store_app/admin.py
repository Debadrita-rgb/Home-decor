from django.contrib import admin
from .models import Slider,Category,Product,Contact

# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display=['id','image','is_active']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','cat_name','cat_image','no_of_products','is_active']

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','pname','price']

class ContactAdmin(admin.ModelAdmin):
    list_display=['id','name','name','mobile','message','status']


admin.site.register(Slider,SliderAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact,ContactAdmin)


