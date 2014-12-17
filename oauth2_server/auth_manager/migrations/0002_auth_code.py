# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='auth_code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=64)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('client_id', models.ForeignKey(to='auth_manager.client_info')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
