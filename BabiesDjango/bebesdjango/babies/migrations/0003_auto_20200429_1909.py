# Generated by Django 3.0.5 on 2020-04-29 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parents', '0001_initial'),
        ('babies', '0002_baby_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baby',
            name='parent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='parents.Parent'),
        ),
    ]
