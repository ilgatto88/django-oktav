# Generated by Django 2.2.5 on 2020-02-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='label',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
