# Generated by Django 3.0.3 on 2020-05-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200321_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='description',
            field=models.CharField(default='null', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='dp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
