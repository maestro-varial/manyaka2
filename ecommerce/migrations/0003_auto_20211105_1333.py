# Generated by Django 3.2.7 on 2021-11-05 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20211105_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='vendors',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='vendor',
        ),
    ]
