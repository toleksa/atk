# Generated by Django 3.1.6 on 2021-02-23 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atk', '0014_externalsite'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitebabe',
            name='tags',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
