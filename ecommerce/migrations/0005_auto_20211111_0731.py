# Generated by Django 3.2.7 on 2021-11-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20211111_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='footprint',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
