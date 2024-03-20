from django.urls import path
from . import views

app_name = 'api'

urlpatterns=[
    path('category/', views.list_category),
    path('create-category/', views.create_category),
    path('product/', views.product_all),
    path('product-detail/<int:id>', views.product_detail),
    path('product-wish/', views.product_wishlist),
    path('product-review/', views.product_review),
    path('register/', views.register),

]