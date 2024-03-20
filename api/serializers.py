from rest_framework.serializers import ModelSerializer
from main.models import (Category, Product, ProductImage, WishList, ProductReview,
                        Cart, CartProduct,Order,OrderItem,User)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1    

    

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'


class ProductReviewSerializer(ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class CartSerializer(ModelSerializer):
    class Meta:
        
        model = Cart
        fields = '__all__'


class CartProductSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CartProduct
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = OrderItem
        fields = '__all__'
    
