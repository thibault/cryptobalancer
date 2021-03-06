# Generated by Django 2.0.3 on 2018-03-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20180318_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='target',
            field=models.DecimalField(decimal_places=2, help_text='How much does this asset should weight in your portfolio?', max_digits=8, verbose_name='Target'),
        ),
    ]
