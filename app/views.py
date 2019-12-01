from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.mixins import UpdateModelMixin

from .models import PizzaType, Order, Pizza
from .serializers import PizzaTypeSerializer, OrderSerializer, PizzaSerializer
from .utils.constants import Constant
from .utils.response import CustomResponse
from .utils.helper import UtilMethods


class OrderAPIView(viewsets.GenericViewSet):
    serializer_class = OrderSerializer

    def get_object(self):
        order = Order.objects.filter(id=self.kwargs.get('pk'))
        return order.first() if order.exists() else None

    def get_queryset(self):
        """
        Optionally restricts the returned orders,
        by filtering against a `status` and `customer` query parameter in the URL.
        """
        queryset = Order.objects.all()
        delivery_status = self.request.query_params.get('status', None)
        phone_number = self.request.query_params.get('customer', None)
        if delivery_status is not None:
            queryset = queryset.filter(status=delivery_status)
        elif phone_number is not None:
            queryset = queryset.filter(order_by__phone_number=phone_number)
        return queryset

    def create(self, request, *args, **kwargs):
        """
          Add order:

          Example data :
            {
              "pizza": [
                        {
                            "flavour": "margarita",
                            "size": "large",
                            "quantity": 1
                         },

                         {
                            "type": "salami",
                            "size": "small",
                            "quantity": 1
                         }

                    ]
              "order_by": {
                        "username": "mirza",
                        "phone_number": "923231489234",
                        "address": "xyz location"
                    }
            }
          """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(
                message=Constant.response.OPERATION_SUCCESS.format(object="Order", operation="placed"),
                data=serializer.data
            ).response()
        return CustomResponse(
            has_error=False,
            code=status.HTTP_400_BAD_REQUEST, message=Constant.response.INVALID_DATA
        ).response()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serialized = self.get_serializer(page, many=True)
        return self.get_paginated_response(serialized.data)

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        if order:
            serialized = self.get_serializer(order)
            return CustomResponse(data=serialized.data).response()
        return CustomResponse(
            code=status.HTTP_404_NOT_FOUND, message=Constant.response.NOT_FOUND.format(object='Order')
        ).response()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        status = request.data.get('status')
        if order and status in dict(Constant.model.STATUS_CHOICES).keys():
            order.status = status
            order.save()
            return CustomResponse(
                message=Constant.response.OPERATION_SUCCESS.format(object='Status', operation='changed')).response()
        return CustomResponse(code=status.HTTP_400_BAD_REQUEST, has_error=False,
                              message=Constant.response.INVALID_DATA).response()

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order:
            order.pizza.all().delete()
            order.delete()
            return CustomResponse(
                message=Constant.response.OPERATION_SUCCESS.format(object='Order', operation='removed')).response()
        return CustomResponse(message=Constant.response.NOT_FOUND.format(object='Order')).response()

    def get_serializer_context(self):
        context = super(OrderAPIView, self).get_serializer_context()
        context.update({'status': UtilMethods.str_to_bool(self.request.GET.get('status', False))})
        return context


class PizzaAPIView(generics.GenericAPIView, UpdateModelMixin):
    serializer_class = PizzaSerializer

    def get_object(self):
        pizza = Pizza.objects.filter(id=self.kwargs.get('pizza'))
        return pizza.first() if pizza.exists() else None

    def put(self, request, *args, **kwargs):
        serialized = self.partial_update(request, *args, **kwargs)
        return CustomResponse(data=serialized.data).response()

    def get_serializer_context(self):
        context = super(PizzaAPIView, self).get_serializer_context()
        context.update({'method': 'PUT'})
        return context


class TypeAPIView(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving pizza types.
    """
    def list(self, request):
        queryset = PizzaType.objects.all()
        serialized = PizzaTypeSerializer(queryset, many=True)
        return CustomResponse(data=serialized.data).response()
