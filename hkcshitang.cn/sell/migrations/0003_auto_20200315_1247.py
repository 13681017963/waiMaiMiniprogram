# Generated by Django 2.2.5 on 2020-03-15 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0002_auto_20200315_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=100, verbose_name='电话'),
        ),
    ]
