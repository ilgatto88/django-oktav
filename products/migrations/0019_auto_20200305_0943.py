# Generated by Django 3.0.3 on 2020-03-05 09:43

from django.db import migrations, models
import products.storage


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_remove_analysis_request_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='file',
            field=models.FileField(storage=products.storage.OverWriteStorage(), upload_to=''),
        ),
    ]
