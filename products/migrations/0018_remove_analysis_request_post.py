# Generated by Django 3.0.3 on 2020-03-04 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_analysis_request_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='request_post',
        ),
    ]
