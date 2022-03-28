# Generated by Django 4.0.3 on 2022-03-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('BW', 'Bottom Wear'), ('TW', 'Top Wear'), ('M', 'Mobile'), ('L', 'Laptop'), ('B', 'Book')], max_length=2),
        ),
    ]
