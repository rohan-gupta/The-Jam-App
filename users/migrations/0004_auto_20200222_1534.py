# Generated by Django 3.0.3 on 2020-02-22 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_spotifyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuser',
            name='refresh_token',
            field=models.CharField(max_length=200),
        ),
    ]
