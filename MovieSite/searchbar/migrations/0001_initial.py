# Generated by Django 3.0.3 on 2020-09-07 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('introduction', models.TextField()),
                ('picutre_src', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=20)),
                ('star', models.CharField(max_length=20)),
                ('birthday', models.CharField(max_length=20)),
                ('birthplace', models.CharField(max_length=50)),
                ('co_actors', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('introduction', models.TextField()),
                ('picutre_src', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('length', models.CharField(max_length=100)),
                ('comments', models.TextField()),
                ('actors', models.ManyToManyField(to='searchbar.Actor')),
            ],
        ),
    ]
