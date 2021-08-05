# Generated by Django 3.2.3 on 2021-06-22 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('mcid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('scid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField(default=0)),
                ('finalPrice', models.IntegerField(default=0)),
                ('instock', models.BooleanField(default=True)),
                ('xs', models.BooleanField(default=True)),
                ('s', models.BooleanField(default=True)),
                ('m', models.BooleanField(default=True)),
                ('l', models.BooleanField(default=True)),
                ('xl', models.BooleanField(default=True)),
                ('color1', models.BooleanField(default=True)),
                ('color2', models.BooleanField(default=True)),
                ('color3', models.BooleanField(default=True)),
                ('color4', models.BooleanField(default=True)),
                ('color5', models.BooleanField(default=True)),
                ('color6', models.BooleanField(default=True)),
                ('color7', models.BooleanField(default=True)),
                ('img1', models.ImageField(upload_to='images')),
                ('img2', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('img3', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('img4', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('date', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.brand')),
                ('maincat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.maincategory')),
                ('subcat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.subcategory')),
            ],
        ),
    ]