# Generated by Django 2.2.5 on 2020-02-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_parameter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('print_name', models.CharField(max_length=100)),
            ],
        ),
    ]
