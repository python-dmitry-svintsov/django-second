from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('my_auth.urls', 'my_auth'), namespace='my_auth')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('tank/', include(('tank.urls', 'tank'), namespace='tank')),
    path('lapi/', include(('lapi.urls', 'lapi'), namespace='lapi'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)