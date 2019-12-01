# Generated by Django 2.2.7 on 2019-11-29 02:04

import app.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', app.models.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', app.models.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('username', models.CharField(max_length=50, verbose_name='User name')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name')),
                ('phone_number', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PizzaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavour', models.CharField(choices=[('margarita', 'Margarita Flavour Pizza'), ('marinara', 'Marinara Flavour Pizza'), ('salami', 'Salami Flavour Pizza')], default='margarita', max_length=50, verbose_name='Flavour')),
                ('size', models.CharField(choices=[('small', 'Small Pizza'), ('medium', 'Medium Pizza'), ('large', 'Large Pizza')], default='small', max_length=10, verbose_name='Size')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Pizza cost $USD')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', app.models.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', app.models.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('total_amount', models.FloatField(blank=True, null=True, verbose_name='Price $USD')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(20)])),
                ('pizza_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='app.PizzaType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', app.models.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', app.models.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('waiting', 'Waiting in queue'), ('preparing', 'Order in Progress'), ('dispatch', 'On way to delivery'), ('delivered', 'Order delivered'), ('cancel', 'Order cancelled')], default='waiting', max_length=50, verbose_name='Order Status')),
                ('payment_type', models.CharField(choices=[('cash', 'Cash on delivery'), ('card', 'Credit card payment')], default='cash', max_length=10, verbose_name='Payment type')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('order_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_customer', to='app.Customer')),
                ('pizza', models.ManyToManyField(related_name='order_pizza', to='app.Pizza')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
