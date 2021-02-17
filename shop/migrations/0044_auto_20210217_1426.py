# Generated by Django 3.1.4 on 2021-02-17 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0043_auto_20210217_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='payment_option',
        ),
        migrations.AlterField(
            model_name='address',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
