from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns=[
    path('',views.index, name = 'index'),
    path('contact',views.contact, name = 'contact'),
    path('cart',views.cart, name ='cart'),
    path('updatecart',views.updateCart),
    path('updatequantity',views.updateQuantity),
    path('login/',views.signin, name='login'),
    path('register/',views.register, name='register'),
    path('searchresults',views.searchbar, name='searchbar'),
    path('signout',views.signout,name='signout'),
    path('checkout', views.checkout, name = 'checkout'),
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)