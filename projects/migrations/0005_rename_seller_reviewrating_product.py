# Generated by Django 3.2.5 on 2022-04-26 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20220424_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='seller',
            new_name='product',
        ),
    ]
