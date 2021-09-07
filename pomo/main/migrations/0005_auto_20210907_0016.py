# Generated by Django 3.2.7 on 2021-09-07 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_item_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cast',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='imdbRating',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='metascore',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='plot',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='poster_link',
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='released',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='runtime',
            field=models.CharField(max_length=100, null=True),
        ),
    ]