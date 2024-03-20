from django.contrib import admin
from . import models


admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.WishList)
admin.site.register(models.ProductReview)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
