from django.urls import path
from . import views

app_name = 'api'

urlpatterns=[
     #auth
    path('login', views.sign_in),
    path('register', views.register),
    path('logout', views.sign_out),
    path('sign', views.sign_up),
    #category CRUD
    path('category-list', views.list_category),
    path('category-create', views.create_category),
    path('category-update/<int:id>', views.category_update),
    path('category-delete/<int:id>', views.category_delete),
    #product CRUD
    path('product-list', views.product_all),
    path('product-create', views.product_create),
    path('product-detail/<int:id>', views.product_detail),
    #Cart
    path('cart-create', views.cart_create),
    path('cart-detail', views.cart_detail),
    path('cart-delete/<int:id>', views.cart_delete),
    #Cart Product
    path('add-to-cart/<int:id>', views.add_to_cart),
    path('delete-cart/<int:id>', views.delete_cart), 
    path('cart-product-detail/<int:id>', views.cart_product_detail), 
    #order
    path('order-create', views.create_order),
    path('order-detail', views.get_order),
    path('order-status-update/<int:id>', views.update_order),
    path('cancel-order/<int:id>', views.delete_order),
    #wishlist
    path('add-wish', views.add_to_wishlist),
    path('remove-wish', views.remove_from_wishlist),
    path('user-wishlist', views.user_wishlist),
    #product review
    path('add-product-review', views.add_product_review),

]