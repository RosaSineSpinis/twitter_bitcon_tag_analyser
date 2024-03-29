# Generated by Django 3.2.7 on 2023-02-28 00:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin_tag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daymodel',
            name='tag_datetime',
            field=models.DateTimeField(default=False),
        ),
        migrations.AlterField(
            model_name='monthmodel',
            name='tag_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='monthmodel',
            name='tag_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='monthmodel',
            name='tag_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
