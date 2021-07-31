# Generated by Django 3.2.5 on 2021-07-31 14:37

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
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('x_pos', models.IntegerField()),
                ('z_pos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnchantmentLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EnchantmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('type', models.CharField(max_length=200)),
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
            name='Potion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PotionModifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PotionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
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
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.business')),
                ('cost_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost', to='app.item')),
                ('stock_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.business')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.business')),
            ],
        ),
        migrations.CreateModel(
            name='PotionModifierToPotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.potion')),
                ('potion_modifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.potionmodifier')),
            ],
        ),
        migrations.AddField(
            model_name='potion',
            name='potion_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.potiontype'),
        ),
        migrations.AddField(
            model_name='potion',
            name='stock_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stockrecord'),
        ),
        migrations.CreateModel(
            name='ItemIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enchanted', models.BooleanField(default=False)),
                ('icon', models.CharField(max_length=200)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('potion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.potiontype')),
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
            name='Enchantment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enchantment_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enchantmentlevel')),
                ('enchantment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enchantmenttype')),
                ('stock_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stockrecord')),
            ],
        ),
        migrations.AddField(
            model_name='business',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.businesstype'),
        ),
    ]
