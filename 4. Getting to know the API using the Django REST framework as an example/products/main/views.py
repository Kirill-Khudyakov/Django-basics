from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from main.serializers import ReviewSerializer, ProductListSerializer, ProductDetailsSerializer
from .models import Product, Review


@api_view(['GET'])
def products_list_view(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
    


class ProductDetailsView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data)       

# доп задание:
class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        mark = request.query_params.get('mark', None)

        # Фильтруем отзывы по product_id
        if mark is not None:
            try:
                mark = int(mark)  # Преобразуем mark в целое число
            except ValueError:
                return Response({"error": "Invalid mark value."}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем отзывы по продукту с заданной оценкой
            reviews = Review.objects.filter(product_id=product_id, mark=mark)
        else:
            # Если mark не указан, возвращаем все отзывы для данного товара
            reviews = Review.objects.filter(product_id=product_id)

        # Сериализация полученных отзывов
        serializer = ReviewSerializer(reviews, many=True)
        
        # Возвращаем отсериализованные данные
        return Response(serializer.data)
