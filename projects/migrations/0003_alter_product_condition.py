# Generated by Django 4.0.2 on 2022-03-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('G', 'Good'), ('O', 'old'), ('N', 'New')], max_length=2),
        ),
    ]
