# Generated by Django 3.2.5 on 2021-07-01 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=64)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=60, unique=True)),
                ('account', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=60)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('type', models.CharField(choices=[('outflow', 'outflow'), ('inflow', 'inflow')], max_length=16)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.user')),
            ],
        ),
    ]