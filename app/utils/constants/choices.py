class ModelChoices(object):
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

    STATUS_CHOICES = (
        ('waiting', 'Waiting in queue'),
        ('preparing', 'Order in Progress'),
        ('dispatch', 'On way to delivery'),
        ('delivered', 'Order delivered'),
        ('cancel', 'Order cancelled')
    )


