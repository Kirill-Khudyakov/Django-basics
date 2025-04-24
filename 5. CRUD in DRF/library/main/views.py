from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Book, Order
from main.serializers import BookSerializer, OrderSerializer


@api_view(['GET'])
def books_list(request):
    """получите список книг из БД
    отсериализуйте и верните ответ
    """
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


class CreateBookView(APIView):
    def post(self, request):
        # получите данные из запроса
        serializer = BookSerializer(data=request.data) #передайте данные из запроса в сериализатор
        if serializer.is_valid(raise_exception=True): #если данные валидны
            serializer.save
            return Response('Книга успешно создана') # возвращаем ответ об этом


class BookDetailsView(RetrieveAPIView):
    # реализуйте логику получения деталей одного объявления
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(UpdateAPIView):
    # реализуйте логику обновления объявления
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_update(self, update):
        update.save()


class BookDeleteView(DestroyAPIView):
    # реализуйте логику удаления объявления
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Книга успешно удалена'}
        )


class OrderViewSet(viewsets.ModelViewSet):
    # реализуйте CRUD для заказов
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Заказ успешно удален'}
        )
