# Generated by Django 2.2.5 on 2019-11-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0036_auto_20191113_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familydoctorvotes',
            name='vote',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='can_vote',
            field=models.IntegerField(default=False),
        ),
    ]