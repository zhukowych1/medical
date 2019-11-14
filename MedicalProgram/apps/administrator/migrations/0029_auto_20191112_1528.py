# Generated by Django 2.2.5 on 2019-11-12 15:28

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0028_auto_20191111_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='key',
        ),
        migrations.AddField(
            model_name='doctor',
            name='key2',
            field=fernet_fields.fields.EncryptedCharField(max_length=3, null=True),
        ),
    ]
