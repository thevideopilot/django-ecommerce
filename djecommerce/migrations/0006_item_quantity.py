# Generated by Django 2.2 on 2020-05-10 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djecommerce', '0005_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
