# Generated by Django 2.2.4 on 2020-06-18 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0016_orderitem_ordered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='ordered',
            new_name='orderedadfa',
        ),
    ]
