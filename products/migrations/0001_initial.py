# Generated by Django 2.2.5 on 2020-02-17 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('print_name', models.CharField(max_length=100)),
                ('function', models.CharField(max_length=100)),
                ('dataset', models.CharField(max_length=100)),
                ('selectable_rcp', models.BooleanField()),
                ('output_types', models.CharField(max_length=100)),
                ('widgets', models.CharField(default='', max_length=100)),
                ('extra', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('widget_type', models.CharField(max_length=100)),
                ('label', models.CharField(default='', max_length=100, null=True)),
                ('enabled', models.BooleanField()),
            ],
        ),
    ]
