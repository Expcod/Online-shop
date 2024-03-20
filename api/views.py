from main import models
from api import serializers
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


#category crud

@api_view(['GET'])
def list_category(request):
    categories = models.Category.objects.all()
    category_ser = serializers.CategorySerializer(categories, many=True)
    print(category_ser.data)
    return Response(category_ser.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_category(request):
    data=request.data
    serializer=serializers.CategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_update(request, id):
    name = request.data['name']
    category = models.Category.objects.get(id = id)
    category.name = name
    category.save()
    category_ser = serializers.CategorySerializer(category)
    return Response({'success' : 'updated',
                     'updated_to' : category_ser.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_delete(request, id):
    category = models.Category.objects.get(id = id).delete()
    return Response({'success' : 'deleted'})

# crud product

@api_view(['GET'])
def product_all(request):
    products=models.Product.objects.all()
    print(products)
    products_ser=serializers.ProductSerializer(products,many=True)
    print(products_ser.data)
    return Response(products_ser.data)


@api_view(['GET'])
def product_detail(request,id):
    product=models.Product.objects.get(id=id)
    product_ser=serializers.ProductSerializer(product)
    return Response(product_ser.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_create(request):
    name = request.data['name']
    description = request.data['description']
    price = request.data['price']
    quantity = request.data['quantity']
    category_id = request.data['category_id']
    banner_img = request.FILES.get('banner')
    category = models.Category.objects.get(id = category_id)
    product = models.Product.objects.create(
        name = name,
        description = description,
        price = price,
        quantity = quantity,
        banner = banner_img,
        category = category,
        author = request.user
    )
    product_ser = serializers.ProductSerializer(product)
    return Response(product_ser.data)

#crud wishlist

@api_view(['POST'])
def product_wishlist(request):
    serializer=serializers.WishlistSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def product_review(request):
    serializer=serializers.ProductReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

#crud cart
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_create(request):
    user = request.user
    if not models.Cart.objects.filter(user = user, is_active = True).first():
        cart = models.Cart.objects.create(
            user = user,
            is_active = True
        )
        cart_ser = serializers.CartSerializer(cart)
        return Response({'success':'created', 'data':cart_ser.data})
    else:
        data = models.Cart.objects.get(user = user, is_active = True)
        serializer = serializers.CartSerializer(data)
        return Response({'fatal':'you already have active cart', 'data':serializer.data})
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_delete(request, id):
    models.Cart.objects.get(id = id, user = request.user).delete()
    return Response({'success':'deleted'})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = models.Cart.objects.get(user = request.user, is_active = True)
    serializer = serializers.CartSerializer(cart)
    return Response(serializer.data)

# cart product

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request, id):
    if request.data.get('quantity'):
        quantity = int(request.data.get('quantity'))
    else:
        quantity = 1
    product = models.Product.objects.get(id = id)
    cart, _ = models.Cart.objects.get_or_create(user = request.user, is_active = True)
    cartproduct = models.CartProduct.objects.filter(cart = cart, product = product).first()
    if cartproduct:
        cartproduct.quantity += quantity
        cartproduct.save()
    else:
        cartproduct = models.CartProduct.objects.create(
            cart = cart,
            product = product,
            quantity = quantity
        )
    serializer = serializers.CartProductSerializer(cartproduct)
    return Response({'success':'created', 'data': serializer.data})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cart(request, id):
    cart_product = models.CartProduct.objects.get(id = id)
    quantity = 1
    if request.data.get('quantity'):
        if request.data.get('quantity') == 'all':
            cart_product.delete()
            return Response({'success':'deleted'})
        
        elif int(request.data.get('quantity')) >= cart_product.quantity:
            cart_product.delete()
            return Response({'success':'deleted'})
        
        else:
            quantity = int(request.data.get('quantity'))

    elif quantity == cart_product.quantity:
        cart_product.delete()
        return Response({'success':'deleted'})

    cart_product.quantity -= quantity
    cart_product.save()
    serializer = serializers.CartProductSerializer(cart_product)
    return Response({'success': f'quantity reduced by {quantity}', 'cart_product' : serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_detail(request, id):
    cart_product = models.CartProduct.objects.get(id = id)
    serializer = serializers.CartProductSerializer(cart_product)
    return Response(serializer.data)

#ordering

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = serializers.OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    try:
        order = models.Order.objects.get(id=order_id)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
    except models.Order.DoesNotExist:
        return Response(status=404)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        return Response(status=404)
    
    serializer = serializers.OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        return Response(status=404)
    
    order.delete()
    return Response(status=204)

#wishlist

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    serializer = serializers.WishListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, user_id, product_id):
    try:
        wishlist_item = serializers.WishList.objects.get(user_id=user_id, product_id=product_id)
        wishlist_item.delete()
        return Response(status=204)
    except serializers.WishList.DoesNotExist:
        return Response(status=404)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_wishlist(request, user_id):
    wishlist_items = serializers.WishList.objects.filter(user_id=user_id)
    serializer = serializers.WishListSerializer(wishlist_items, many=True)
    return Response(serializer.data)

#product review
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product_review(request):
    serializer = serializers.ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        """Foydalanuvchi va maxsulot uchun tahlilni tekshirish"""
        user = request.data.get('user')
        product = request.data.get('product')
        existing_review = serializers.ProductReview.objects.filter(user=user, product=product).first()
        if existing_review:
            existing_review.delete()  # Eski tahlilni ochirish
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

#Auth

@api_view(['POST'])
def sign_up(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')  
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        if password == password_confirm:
            user = User.objects.create_user(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = serializer.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    new_username = request.data.get('new_username')
    new_password = request.data.get('new_password')
    
    if new_username and new_password:
        user.username = new_username
        user.set_password(new_password)        
        user.save()
        return Response({'message': 'User data updated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'New user data not provided.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully signed out'}, status=status.HTTP_200_OK)


    


