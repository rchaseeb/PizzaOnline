from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Pizza, Customer, Order, PizzaType


class OrderTests(APITestCase):
    """
    Create Order object for testing purpose.
    """
    def setUp(self):
        pizza_type = PizzaType.objects.create(flavour="salami", size="small", price=13.0)
        self.pizza = Pizza(pizza_type=pizza_type, quantity=3)
        self.pizza.save()
        customer = Customer.objects.create(username='test', address='Lahore, Pakistan', phone_number=1352532341)
        self.order = Order.objects.create(order_by=customer)
        self.order.pizza.add(self.pizza)
        self.order.save()

    def test_list_orders(self):
        """
        Ensure the orders list working.
        """

        url = reverse('orders-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        """
        Delete order bu providing order id.
        """

        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
