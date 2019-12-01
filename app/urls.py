from django.urls import path
from app.views import TypeAPIView, PizzaAPIView, OrderAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'order', OrderAPIView, basename='orders')
router.register(r'types', TypeAPIView, basename='pizza-types')

urlpatterns = [
    path('pizza/<int:pizza>/', PizzaAPIView.as_view(), name='update-pizza')
]

urlpatterns += router.urls
