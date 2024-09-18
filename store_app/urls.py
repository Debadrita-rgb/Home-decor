from django.urls import path
from store_app import views
from django.conf.urls.static import static
from store import settings

urlpatterns = [
    path('',views.index),
    path('category_details/<cid>',views.category_details),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid>',views.add_to_cart),
    path('addtowishlist/<pid>',views.add_to_wishlist),
    path('view_wishlist',views.view_wishlist),
    path('view_cart',views.view_cart),
    path('my_address',views.my_address),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('category_details/<cid>/range',views.range),
    path('category_details/<cid>/sort/<sv>',views.sort),
    path('addtocart_cat/<pid>/<cid>',views.addtocart_cat),

    path('deleteaddress/<aid>',views.deleteaddress),
    path('setasdefault/<aid>',views.setasdefault),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('remove/<cid>',views.remove_product),
    path('place_order',views.place_order),
    path('remove_oqty/<oid>',views.remove_oqty),
    # path('use_address',views.use_address),
    path('order_history',views.order_history),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail),
    path('about',views.about),
    path('privacy',views.privacy),
    path('contact',views.contact),
    path('newsletter',views.newsletter)

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)