# Generated by Django 5.0.1 on 2024-08-19 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to='images/products')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Описание товара',
                'verbose_name_plural': 'Описания товара',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/direction')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Направление товаров',
                'verbose_name_plural': 'Направления товаров',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.description')),
            ],
        ),
        migrations.CreateModel(
            name='SubDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/subdirection')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.direction')),
            ],
            options={
                'verbose_name': 'Поднаправление товаров',
                'verbose_name_plural': 'Поднаправления товаров',
            },
        ),
        migrations.AddField(
            model_name='description',
            name='subdirection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.subdirection'),
        ),
    ]