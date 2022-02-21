# Generated by Django 3.2.7 on 2022-02-10 23:26

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_dictionary', picklefield.fields.PickledObjectField(editable=False)),
                ('tag_date', models.DateField(auto_now_add=True)),
                ('tag_time', models.TimeField(auto_now_add=True)),
                ('tag_datetime', models.DateTimeField(auto_now_add=True)),
                ('beginning_datetime', models.DateTimeField(null=True)),
                ('ending_datetime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_dictionary', picklefield.fields.PickledObjectField(editable=False)),
                ('tag_date', models.DateField()),
                ('tag_time', models.TimeField()),
                ('tag_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MonthModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_dictionary', picklefield.fields.PickledObjectField(editable=False)),
                ('tag_date', models.DateField(auto_now_add=True)),
                ('tag_time', models.TimeField(auto_now_add=True)),
                ('tag_datetime', models.DateTimeField(auto_now_add=True)),
                ('beginning_datetime', models.DateTimeField()),
                ('ending_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.TextField(default='aaa', max_length=200)),
                ('user_surname', models.CharField(default='missing', max_length=200)),
            ],
        ),
    ]
