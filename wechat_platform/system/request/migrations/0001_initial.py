# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestEvent',
            fields=[
                ('eventid', models.CharField(max_length=50, serialize=False, verbose_name='\u4e8b\u4ef6ID', primary_key=True)),
                ('target', models.CharField(max_length=50, verbose_name='\u76ee\u6807\u7528\u6237OpenID')),
                ('source', models.CharField(max_length=50, verbose_name='\u6765\u6e90\u7528\u6237OpenID')),
                ('time', models.IntegerField(verbose_name='\u4fe1\u606f\u53d1\u9001\u65f6\u95f4')),
                ('type', models.CharField(blank=True, max_length=15, null=True, verbose_name='\u4e8b\u4ef6\u7c7b\u578b', choices=[(b'subscribe', '\u8ba2\u9605\u4e8b\u4ef6'), (b'unsubscribe', '\u53d6\u6d88\u8ba2\u9605\u4e8b\u4ef6'), (b'click', '\u70b9\u51fb\u4e8b\u4ef6'), (b'location', '\u5730\u7406\u4f4d\u7f6e\u4e8b\u4ef6')])),
                ('key', models.TextField(null=True, verbose_name='\u4e8b\u4ef6key\u503c', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u4e8b\u4ef6-\u7eac\u5ea6', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u4e8b\u4ef6-\u7ecf\u5ea6', blank=True)),
                ('precision', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u4e8b\u4ef6-\u7cbe\u5ea6', blank=True)),
            ],
            options={
                'db_table': 'request_event',
                'verbose_name': '\u5fae\u4fe1\u670d\u52a1\u5668\u8bf7\u6c42\u4e8b\u4ef6',
                'verbose_name_plural': '\u5fae\u4fe1\u670d\u52a1\u5668\u8bf7\u6c42\u4e8b\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestMessage',
            fields=[
                ('msgid', models.CharField(max_length=25, serialize=False, verbose_name='\u6d88\u606fID', primary_key=True)),
                ('target', models.CharField(max_length=50, verbose_name='\u76ee\u6807\u7528\u6237OpenID')),
                ('source', models.CharField(max_length=50, verbose_name='\u6765\u6e90\u7528\u6237OpenID')),
                ('time', models.IntegerField(verbose_name='\u4fe1\u606f\u53d1\u9001\u65f6\u95f4')),
                ('raw', models.TextField(verbose_name='\u4fe1\u606f\u539f\u59cbXML\u5185\u5bb9')),
                ('type', models.CharField(max_length=15, verbose_name='\u4fe1\u606f\u7c7b\u578b', choices=[(b'text', '\u6587\u672c\u6d88\u606f'), (b'image', '\u56fe\u7247\u6d88\u606f'), (b'video', '\u89c6\u9891\u6d88\u606f'), (b'link', '\u94fe\u63a5\u6d88\u606f'), (b'location', '\u5730\u7406\u4f4d\u7f6e\u6d88\u606f'), (b'voice', '\u8bed\u97f3\u6d88\u606f')])),
                ('text_content', models.TextField(null=True, verbose_name='\u6587\u672c\u6d88\u606f-\u4fe1\u606f\u5185\u5bb9', blank=True)),
                ('image_picurl', models.URLField(null=True, verbose_name='\u56fe\u7247\u6d88\u606f-\u56fe\u7247\u7f51\u5740', blank=True)),
                ('video_media_id', models.CharField(max_length=50, null=True, verbose_name='\u89c6\u9891\u6d88\u606f-\u5a92\u4f53ID', blank=True)),
                ('video_thumb_media_id', models.CharField(max_length=50, null=True, verbose_name='\u89c6\u9891\u6d88\u606f-\u7f29\u7565\u56fe\u5a92\u4f53ID', blank=True)),
                ('link_title', models.CharField(max_length=80, null=True, verbose_name='\u94fe\u63a5\u6d88\u606f-\u6807\u9898', blank=True)),
                ('link_description', models.TextField(null=True, verbose_name='\u94fe\u63a5\u6d88\u606f-\u63cf\u8ff0', blank=True)),
                ('link_url', models.URLField(null=True, verbose_name='\u94fe\u63a5\u6d88\u606f-\u94fe\u63a5', blank=True)),
                ('location_x', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u6d88\u606f-\u7eac\u5ea6', blank=True)),
                ('location_y', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u6d88\u606f-\u7ecf\u5ea6', blank=True)),
                ('location_scale', models.FloatField(null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u6d88\u606f-\u7f29\u653e\u5927\u5c0f', blank=True)),
                ('location_label', models.CharField(max_length=80, null=True, verbose_name='\u5730\u7406\u4f4d\u7f6e\u6d88\u606f-\u4f4d\u7f6e\u4fe1\u606f', blank=True)),
                ('voice_media_id', models.CharField(max_length=50, null=True, verbose_name='\u8bed\u97f3\u6d88\u606f-\u5a92\u4f53ID', blank=True)),
                ('voice_format', models.CharField(max_length=20, null=True, verbose_name='\u8bed\u97f3\u6d88\u606f-\u58f0\u97f3\u683c\u5f0f', blank=True)),
                ('voice_recognition', models.TextField(null=True, verbose_name='\u8bed\u97f3\u6d88\u606f-\u8bc6\u522b\u7ed3\u679c', blank=True)),
            ],
            options={
                'db_table': 'request_message',
                'verbose_name': '\u5fae\u4fe1\u670d\u52a1\u5668\u8bf7\u6c42\u6d88\u606f',
                'verbose_name_plural': '\u5fae\u4fe1\u670d\u52a1\u5668\u8bf7\u6c42\u6d88\u606f',
            },
            bases=(models.Model,),
        ),
    ]
