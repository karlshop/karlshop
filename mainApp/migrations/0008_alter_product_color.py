# Generated by Django 3.2.3 on 2021-07-07 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_auto_20210707_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, default='red', max_length=20, null=True),
        ),
    ]