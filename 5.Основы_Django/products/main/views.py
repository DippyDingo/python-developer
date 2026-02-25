from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Product, Review
from .serializers import ProductListSerializer, ProductDetailsSerializer, ReviewSerializer

@api_view(['GET'])
def products_list_view(request):
    """реализуйте получение всех товаров из БД
    реализуйте сериализацию полученных данных
    отдайте отсериализованные данные в Response"""
    # 1. Получаем все товары из базы
    products = Product.objects.all()

    # 2. Сериализуем данные.
    # many=True обязательно, так как мы передаем список объектов, а не один!
    serializer = ProductListSerializer(products, many=True)

    # 3. Возвращаем ответ
    return Response(serializer.data)


class ProductDetailsView(APIView):
    def get(self, request, product_id):
        """реализуйте получение товара по id, если его нет, то выдайте 404
        реализуйте сериализацию полученных данных
        отдайте отсериализованные данные в Response"""
        # 1. Ищем товар по id
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # Если не нашли — возвращаем статус 404
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 2. Сериализуем конкретный товар (вместе с вложенными отзывами)
        serializer = ProductDetailsSerializer(product)

        # 3. Возвращаем ответ
        return Response(serializer.data)


# доп задание:
class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        """обработайте значение параметра mark и
        реализуйте получение отзывов по конкретному товару с определённой оценкой
        реализуйте сериализацию полученных данных
        отдайте отсериализованные данные в Response"""
        # 1. Сначала получаем ВСЕ отзывы для конкретного товара
        reviews = Review.objects.filter(product_id=product_id)

        # 2. Достаем параметр mark из адреса (например: ?mark=5)
        # В DRF параметры из URL берутся через request.query_params
        mark = request.query_params.get('mark')

        # 3. Если параметр передали, дополнительно фильтруем отзывы по этой оценке
        if mark is not None:
            reviews = reviews.filter(mark=mark)

        # 4. Сериализуем результат
        serializer = ReviewSerializer(reviews, many=True)

        # 5. Возвращаем ответ
        return Response(serializer.data)
