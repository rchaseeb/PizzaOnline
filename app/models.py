from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


def phone_validator():
    message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    return RegexValidator(regex=r'^\+?1?\d{9,15}$', message=message)


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True


class PizzaType(models.Model):
    FLAVOURS_CHOICES = (
        ('margarita', 'Margarita Flavour Pizza'),
        ('marinara', 'Marinara Flavour Pizza'),
        ('salami', 'Salami Flavour Pizza')
    )

    SIZE_CHOICES = (
        ('small', 'Small Pizza'),
        ('medium', 'Medium Pizza'),
        ('large', 'Large Pizza')
    )
    flavour = models.CharField(_("Flavour"), max_length=50, default='margarita', choices=FLAVOURS_CHOICES)
    size = models.CharField(_("Size"), max_length=10, default='small', choices=SIZE_CHOICES)
    price = models.FloatField(_("Pizza cost $USD"), null=True, blank=True)
    description = models.CharField(_("Description"), max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.flavour}-{self.price}"


class Pizza(TimeStampedModel):
    """
    Class model that provides details of pizza with fields.

    """
    pizza_type = models.ForeignKey(PizzaType, related_name='pizza', on_delete=models.CASCADE)
    total_amount = models.FloatField(_("Price $USD"), null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def save(self, *args, **kwargs):
        self.total_amount = self.pizza_type.price * self.quantity
        super(Pizza, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pizza_type.flavour}-{self.quantity}"


class Customer(TimeStampedModel):
    """
    Class model that provides details of customer with information
    of must ``username`` and ``phone_number`` and ``address`` fields.

    """
    username = models.CharField(_("User name"), max_length=50)
    first_name = models.CharField(_("First name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        validators=[phone_validator()],
        max_length=16, unique=True
    )
    address = models.CharField(_("Address"), max_length=500)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"


class Order(TimeStampedModel):
    """
    Class model that provides details of order with information
    of must ``pizza`` and ``order_by`` fields.

    """
    STATUS_CHOICES = (
        ('waiting', 'Waiting in queue'),
        ('preparing', 'Order in Progress'),
        ('dispatch', 'On way to delivery'),
        ('delivered', 'Order delivered'),
        ('cancel', 'Order cancelled')
    )

    PAYMENT_CHOICES = (
        ('cash', 'Cash on delivery'),
        ('card', 'Credit card payment')
    )

    status = models.CharField(_("Order Status"), max_length=50, default='waiting', choices=STATUS_CHOICES)
    payment_type = models.CharField(_("Payment type"), max_length=10, default='cash', choices=PAYMENT_CHOICES)
    pizza = models.ManyToManyField(Pizza, related_name='order_pizza')
    order_by = models.ForeignKey(Customer, related_name='order_customer', on_delete=models.CASCADE)
    description = models.CharField(_("Description"), max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.order_by}"

# class Address(models.Model):
#     city = models.CharField(max_length=200, null=True, blank=True, default='')
#     state = models.CharField(max_length=200, blank=True, null=True, default='')
#     hometown = models.CharField(max_length=200, blank=True, null=True, default='')
#     country = CountryField(blank_label='(select country)', default='', null=True, blank=True)
#
#     def __str__(self):
#         return '%s - %s - %s' % (
#             self.city.encode('utf-8'), self.state.encode('utf-8'), self.country.code.encode('utf-8'))
#
