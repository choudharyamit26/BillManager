# Generated by Django 2.2.4 on 2020-06-18 17:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0020_auto_20200618_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_id',
            field=models.CharField(default=uuid.uuid4, max_length=10),
        ),
    ]
