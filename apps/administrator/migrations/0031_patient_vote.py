# Generated by Django 2.2.5 on 2019-11-12 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0030_auto_20191112_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='vote',
            field=models.IntegerField(null=True),
        ),
    ]