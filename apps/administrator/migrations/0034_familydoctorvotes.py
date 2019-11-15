# Generated by Django 2.2.5 on 2019-11-12 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0033_delete_familydoctorvotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDoctorVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.Doctor')),
            ],
        ),
    ]