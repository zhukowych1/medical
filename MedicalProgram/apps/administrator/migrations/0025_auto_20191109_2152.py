# Generated by Django 2.2.5 on 2019-11-09 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0024_auto_20191109_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='visiting_template',
        ),
        migrations.DeleteModel(
            name='VisitingsTemplate',
        ),
    ]
