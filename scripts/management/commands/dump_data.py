from django.core.management.base import BaseCommand, CommandError
from app.models import PizzaType


class Command(BaseCommand):
    help = 'Migrate data to Pizza Type table'

    def handle(self, *args, **options):
        data = [
            {'flavour': 'margarita', 'size': 'small', 'price': 4.9, 'description': ''},
            {'flavour': 'margarita', 'size': 'medium', 'price': 10.0, 'description': ''},
            {'flavour': 'margarita', 'size': 'large', 'price': 14.9, 'description': ''},

            {'flavour': 'marinara', 'size': 'small', 'price': 5.9, 'description': ''},
            {'flavour': 'marinara', 'size': 'medium', 'price': 12.0, 'description': ''},
            {'flavour': 'marinara', 'size': 'large', 'price': 17.9, 'description': ''},

            {'flavour': 'salami', 'size': 'small', 'price': 13.0, 'description': ''},
            {'flavour': 'salami', 'size': 'medium', 'price': 15.0, 'description': ''},
            {'flavour': 'salami', 'size': 'large', 'price': 18.9, 'description': ''},
        ]
        data_list = list()
        try:
            for pizza in data:
                data_list.append(PizzaType(**pizza))
            pizza_type = PizzaType.objects.bulk_create(data_list)
        except Exception:
            raise CommandError('Exception occurred while creating objects.')
        self.stdout.write(self.style.SUCCESS('Successfully executed! {} objects added'.format(len(pizza_type))))
