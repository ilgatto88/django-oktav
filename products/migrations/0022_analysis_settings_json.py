# Generated by Django 3.0.3 on 2020-03-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20200305_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='settings_json',
            field=models.TextField(default='', max_length=4096),
        ),
    ]
