# Generated by Django 2.2.5 on 2020-02-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_outputtype_regionoption_scenario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionoption',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
