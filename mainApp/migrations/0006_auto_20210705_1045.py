# Generated by Django 3.2.3 on 2021-07-05 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_seller_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.FileField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img2',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img3',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img4',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='pic',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images'),
        ),
    ]
