# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-27 09:48
from __future__ import unicode_literals

from django.db import migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taiga_contrib_holidays', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankholidays',
            name='days_ignored',
            field=djorm_pgarray.fields.DateArrayField(dbtype='date', default=[], verbose_name='days ignored in burndown'),
        ),
    ]