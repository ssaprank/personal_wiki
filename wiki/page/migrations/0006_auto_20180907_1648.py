# Generated by Django 2.0.6 on 2018-09-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_auto_20180907_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='description',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='images'),
        ),
    ]