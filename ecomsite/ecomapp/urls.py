from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),
    
    path('register/', views.register, name="register"),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutpage, name='logout'),
    
    path('add-to-cart', views.addtocart, name='addtocart'),
    path('cart', views.viewcart, name='cart'),
    path('update-cart', views.updatecart, name="updatecart"),
    path('delete-cart-item', views.deletecartitem, name="deletecartitem"),

    path('wishlist', views.index, name="wishlist"),
    path('add-to-wishlist', views.addtowishlist, name='addtowishlist'),
    path('delete-wishlist-item', views.deletewishlistitem, name="deletewishlistitem"),
    
    path('checkout',views.checkoutview, name='checkoutview'), 
    path('place-order', views.placeorder, name="placeorder"),
    
    path('proceed-to-pay', views.razorpaycheck),
    path('my-orders', views.myorders, name='myorders'),
    path('view-order/<str:t_no>', views.orderview, name='orderview'),

    path('product-list', views.productlist, name='productlist'),
    path('search-product', views.searchproduct, name="searchproduct"),

]
