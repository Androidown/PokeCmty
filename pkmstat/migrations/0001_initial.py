# Generated by Django 3.0.8 on 2020-07-23 08:38

from django.db import migrations, models
import pkmstat.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PokeMon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.PositiveSmallIntegerField()),
                ('form', pkmstat.models.PositiveTinyIntegerField(default=0)),
                ('HP', pkmstat.models.PositiveTinyIntegerField()),
                ('ATK', pkmstat.models.PositiveTinyIntegerField()),
                ('DEF', pkmstat.models.PositiveTinyIntegerField()),
                ('SPA', pkmstat.models.PositiveTinyIntegerField()),
                ('SPD', pkmstat.models.PositiveTinyIntegerField()),
                ('SPE', pkmstat.models.PositiveTinyIntegerField()),
                ('type1', pkmstat.models.PositiveTinyIntegerField()),
                ('type2', pkmstat.models.PositiveTinyIntegerField(null=True)),
                ('ability1', models.PositiveSmallIntegerField(default=0)),
                ('ability2', models.PositiveSmallIntegerField(default=0)),
                ('abilityH', models.PositiveSmallIntegerField(default=0)),
                ('name_CHS', models.CharField(max_length=5)),
            ],
            options={
                'unique_together': {('species', 'form')},
            },
        ),
    ]
