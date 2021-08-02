# Generated by Django 3.2.5 on 2021-08-02 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enchantment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('is_enchantable', models.BooleanField(default=False)),
                ('is_potion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('x_pos', models.IntegerField(null=True)),
                ('y_pos', models.IntegerField(null=True)),
                ('z_pos', models.IntegerField(null=True)),
                ('spawn_distance', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('icon', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Potion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('splash', models.BooleanField(default=False)),
                ('lingering', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_id', models.CharField(max_length=200)),
                ('avatar_hash', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_description', models.CharField(blank=True, max_length=200, null=True)),
                ('stock_stack_size', models.IntegerField()),
                ('cost_description', models.CharField(blank=True, max_length=200, null=True)),
                ('cost_stack_size', models.IntegerField()),
                ('units', models.IntegerField()),
                ('last_updated', models.DateTimeField()),
                ('cost_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost', to='app.item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.location')),
                ('stock_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.location')),
            ],
        ),
        migrations.CreateModel(
            name='PotionToStockRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.potion')),
                ('stock_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stockrecord')),
            ],
        ),
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region'),
        ),
        migrations.CreateModel(
            name='ItemIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enchanted', models.BooleanField(default=False)),
                ('icon', models.CharField(max_length=200)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('potion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.potion')),
            ],
        ),
        migrations.CreateModel(
            name='ItemClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='FarmRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xp', models.BooleanField(default=False)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.location')),
                ('mob', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.mob')),
            ],
        ),
        migrations.CreateModel(
            name='EnchantmentToStockRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enchantment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enchantment')),
                ('stock_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stockrecord')),
            ],
        ),
    ]
