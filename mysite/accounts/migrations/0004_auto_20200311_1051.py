# Generated by Django 2.2.6 on 2020-03-11 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200311_1031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': '重写用户', 'verbose_name_plural': '重写用户'},
        ),
    ]
