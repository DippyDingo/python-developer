from rest_framework import serializers
from .models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов. Отдает все поля."""
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.Serializer):
    """Сериализатор для списка товаров. Отдает только title и price."""

    title = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProductDetailsSerializer(serializers.ModelSerializer):
    """Сериализатор для деталей товара. Включает вложенные отзывы."""

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'reviews']