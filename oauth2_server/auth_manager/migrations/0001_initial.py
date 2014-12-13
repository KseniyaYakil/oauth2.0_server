# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='access_token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=1024)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('refresh_token', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='client_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=1024)),
                ('client_secret', models.CharField(max_length=1024)),
                ('redirect_domain', models.URLField(max_length=1024)),
                ('client_name', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='access_token',
            name='app_id',
            field=models.ForeignKey(to='auth_manager.client_info'),
            preserve_default=True,
        ),
    ]
