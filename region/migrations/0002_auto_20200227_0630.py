# Generated by Django 3.0.3 on 2020-02-27 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundesland',
            name='name',
            field=models.CharField(choices=[('austria', 'Austria'), ('bundesland', 'Bundesland'), ('municipality', 'Municipality')], max_length=100),
        ),
    ]
