# Generated by Django 3.1.4 on 2021-01-23 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_billingaddress_payment_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('amount', models.FloatField()),
            ],
        ),
    ]
