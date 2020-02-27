# Generated by Django 3.0.3 on 2020-02-27 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0002_auto_20200227_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundesland',
            name='name',
            field=models.CharField(choices=[('burgenland', 'Burgenland'), ('niederösterreich', 'Niederösterreich'), ('oberösterreich', 'Oberösterreich'), ('wien', 'Wien'), ('steiermark', 'Steiermark'), ('tirol', 'Tirol'), ('kärnten', 'Kärnten'), ('salzburg', 'Salzburg'), ('vorarlberg', 'Vorarlberg')], max_length=50),
        ),
    ]
