# Generated by Django 2.2.6 on 2020-03-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(choices=[('0', '运营商故障'), ('1', '机房故障'), ('2', '程序故障')], max_length=255, unique=True, verbose_name='故障类型'),
        ),
    ]