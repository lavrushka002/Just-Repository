# Generated by Django 3.0.8 on 2020-07-23 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0003_auto_20200721_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='item',
            field=models.CharField(max_length=300, verbose_name='item'),
        ),
        migrations.AlterField(
            model_name='resultresponse',
            name='gems',
            field=models.CharField(max_length=300, verbose_name='gems'),
        ),
    ]