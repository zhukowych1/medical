# Generated by Django 2.2.5 on 2019-10-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_auto_20191021_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='conclusion',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
