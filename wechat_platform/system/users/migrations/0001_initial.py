# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('email', models.EmailField(max_length=255, verbose_name='\u7535\u5b50\u90ae\u4ef6\u5730\u5740')),
                ('nickname', models.CharField(max_length=30, verbose_name='\u6635\u79f0')),
                ('is_active', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u8d85\u7ea7\u7ba1\u7406\u5458')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6ce8\u518c\u65e5\u671f')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'db_table': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserOfficialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(verbose_name='\u6240\u5c5e\u7528\u6237\u7ec4', to='auth.Group')),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u5fae\u4fe1\u516c\u4f17\u8d26\u53f7', to='official_account.OfficialAccount')),
                ('user', models.ForeignKey(verbose_name='\u6240\u5c5e\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
                'db_table': 'user_official_account',
            },
            bases=(models.Model,),
        ),
    ]
