from django.contrib import admin
from .models import Client, Car, Sale

# зарегистрируйте необходимые модели
admin.site.register(Client)
admin.site.register(Car)
admin.site.register(Sale)