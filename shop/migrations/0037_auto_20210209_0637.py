# Generated by Django 3.1.4 on 2021-02-09 06:37

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_refund'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('street_address', models.CharField(max_length=200)),
                ('apartment_address', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=20)),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1)),
                ('default', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('payment_option', models.CharField(blank=True, max_length=10, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.customer')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='shop.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='shop.address'),
        ),
        migrations.DeleteModel(
            name='BillingAddress',
        ),
    ]
