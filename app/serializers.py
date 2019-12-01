from rest_framework import serializers, status
from django.db.models import Sum
from django.utils.timezone import now

from app.models import Order, Pizza, Customer, PizzaType
from app.utils.response import CustomResponse
from app.utils.constants import Constant


class PizzaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaType
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PizzaSerializer(serializers.ModelSerializer):
    pizza_type = PizzaTypeSerializer(read_only=True, many=False)
    flavour = serializers.ChoiceField(choices=['margarita', 'marinara', 'salami'], required=False, write_only=True)
    size = serializers.ChoiceField(choices=['large', 'medium', 'small'], required=False, write_only=True)

    class Meta:
        model = Pizza
        fields = '__all__'

    def validate(self, attrs):
        order = self.instance.order_pizza.first()
        if order.status in ['dispatch', 'delivered', 'cancel']:
            raise CustomResponse(
                message='You cannot edit order with status %s.' % order.status,
                code=status.HTTP_400_BAD_REQUEST
            ).error()
        return attrs

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        data = {
            'flavour': validated_data.get('flavour', instance.pizza_type.flavour),
            'size': validated_data.get('size', instance.pizza_type.size)
        }
        pizza_type = PizzaType.objects.filter(**data).first()
        instance.pizza_type = pizza_type
        instance.save()
        instance.order_pizza.update(modified=now())
        return instance

    def to_representation(self, instance):
        data = super(PizzaSerializer, self).to_representation(instance)
        if self.context.get('method') == 'PUT':
            data = OrderSerializer(instance.order_pizza.first()).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    total_bill = serializers.SerializerMethodField(read_only=True)

    def get_total_bill(self, instance):
        return instance.pizza.all().aggregate(value=Sum('total_amount')).get('value', 0.0)

    class Meta:
        model = Order
        fields = [
            'id', 'total_bill', 'payment_type', 'status', 'description',
            'created', 'modified', 'pizza', 'order_by'
        ]

    def is_valid(self, raise_exception=False):
        data = self.initial_data
        pizza = data.get('pizza', [])
        customer = data.get('order_by')
        if not pizza or not bool(customer):
            raise CustomResponse(
                message='Invalid Format.',
                code=status.HTTP_400_BAD_REQUEST
            ).error()
        return super(OrderSerializer, self).is_valid(raise_exception=True)

    def validate(self, data):
        customer = data.get('order_by')
        pizzas = data.get('pizza')
        if customer.get('phone_number'):
            customer = Customer.objects.filter(phone_number=customer.get('phone_number'))
            if not customer.exists():
                if not customer.get('username') or not customer.get('address'):
                    raise CustomResponse(
                        code=status.HTTP_400_BAD_REQUEST,
                        message='Please give complete customer details', data=None).error()
        for pizza in pizzas:
            if pizza.get('flavour') not in dict(Constant.model.FLAVOURS_CHOICES).keys():
                raise CustomResponse(
                    code=status.HTTP_400_BAD_REQUEST,
                    message='Invalid flavour.', data=None).error()

            if pizza.get('size') not in dict(Constant.model.SIZE_CHOICES).keys():
                raise CustomResponse(
                    code=status.HTTP_400_BAD_REQUEST,
                    message='Invalid size.', data=None).error()

        return data

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        types = PizzaType.objects.all()
        pizza = validated_data.get('pizza')
        customer = validated_data.get('order_by')
        member = Customer.objects.filter(phone_number=customer.get('phone_number'))
        member = Customer.objects.create(**customer) if not member.exists() else member.first()
        data = {
            'order_by': member,
            'payment_type': validated_data.get('payment_type', 'cash'),
            'description': validated_data.get('description')
        }
        order = Order.objects.create(**data)

        for p in pizza:
            pizza_type = types.filter(flavour=p.get('flavour'), size=p.get('size')).first()
            pizza_obj = Pizza(pizza_type=pizza_type, quantity=p.get('quantity'))
            pizza_obj.save()
            order.pizza.add(pizza_obj)
        return order

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        data.update({
            'order_by': CustomerSerializer(instance.order_by).data,
            'pizza': PizzaSerializer(instance.pizza.all(), many=True).data
        })
        if self.context.get('status', False):
            data.pop('pizza')
        return data

