# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-19 09:04
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0061_auto_20181018_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ignoring_weekends', models.NullBooleanField(default=False, verbose_name='is ignoring weekends')),
                ('is_ignoring_days', models.NullBooleanField(default=False, verbose_name='is ignoring specific days')),
                ('days_ignored', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(blank=True, default=None, null=True), blank=True, default=None, null=True, size=None, verbose_name='days ignored in burndown')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bank_holidays', to='projects.Project')),
            ],
        ),
    ]
