# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('official_account', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plugin_iden', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u63d2\u4ef6\u6807\u8bc6\u7b26')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='\u97f3\u4e50\u6807\u9898', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u97f3\u4e50\u63cf\u8ff0', blank=True)),
                ('music_url', models.CharField(max_length=1024, null=True, verbose_name='\u97f3\u4e50URL', blank=True)),
                ('hq_music_url', models.CharField(max_length=1024, null=True, verbose_name='\u9ad8\u6e05\u97f3\u4e50URL', blank=True)),
                ('thumb_media_id', models.CharField(max_length=255, null=True, verbose_name='\u7f29\u7565\u56fe\u5a92\u4f53ID', blank=True)),
                ('hq_music', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u9ad8\u6e05\u97f3\u4e50\u6587\u4ef6', blank=True, to='media.Media', null=True)),
                ('music', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u97f3\u4e50\u6587\u4ef6', blank=True, to='media.Media', null=True)),
                ('official_account', models.ForeignKey(verbose_name='\u6240\u5c5e\u516c\u4f17\u53f7', to='official_account.OfficialAccount')),
                ('thumb', models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u7f29\u7565\u56fe\u5a92\u4f53\u56fe\u50cf', blank=True, to='media.Media', null=True)),
            ],
            options={
                'db_table': 'library_music',
                'verbose_name': '\u7d20\u6750\u5e93 - \u97f3\u4e50\u5e93',
                'verbose_name_plural': '\u7d20\u6750\u5e93 - \u97f3\u4e50\u5e93',
            },
            bases=(models.Model,),
        ),
    ]
