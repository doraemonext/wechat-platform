# -*- coding: utf-8 -*-

import time

from django.core.urlresolvers import reverse
from wechat_sdk import WechatBasic, WechatExt
from rest_framework import serializers

from system.official_account.models import OfficialAccount
from system.media.models import Media
from system.library.news.models import LibraryNews
from system.simulation import Simulation


class LibraryNewsListSeriailzer(serializers.ModelSerializer):
    """
    系统素材库 - 图文库 序列化类 (仅限获取列表信息[GET])
    """
    show_cover_pic = serializers.SerializerMethodField('get_show_cover_pic')
    picurl = serializers.SerializerMethodField('get_picurl')
    content_url = serializers.SerializerMethodField('get_content_url')
    storage_location = serializers.SerializerMethodField('get_storage_location')
    multi_item = serializers.SerializerMethodField('get_multi_item')
    datetime = serializers.SerializerMethodField('get_datetime')

    def get_show_cover_pic(self, obj):
        if obj.picture:
            return True
        else:
            return False

    def get_picurl(self, obj):
        if not obj.picurl or not obj.picture:
            return None
        elif obj.picurl == reverse('filetranslator:download', kwargs={'key': obj.picture.key}):
            return self.context['view'].request.build_absolute_uri(obj.picurl)
        else:
            return obj.picurl

    def get_content_url(self, obj):
        """
        获取文章访问的绝对路径
        """
        if obj.is_simulated():
            return self.context['view'].request.build_absolute_uri(reverse('news:detail', kwargs={'pk': obj.pk}))
        else:
            return obj.url

    def get_storage_location(self, obj):
        multi_item = LibraryNews.manager.get(
            official_account=obj.official_account,
            plugin_iden=obj.plugin_iden,
            root=obj
        )
        for item in multi_item:
            if not item.is_simulated():
                return 'remote'
        return 'local'

    def get_multi_item(self, obj):
        multi_item = LibraryNews.manager.get(
            official_account=obj.official_account,
            plugin_iden=obj.plugin_iden,
            root=obj
        )
        multi_item_expander = []
        for item in multi_item:
            multi_item_expander.append({
                'id': item.pk,
                'title': item.title,
                'description': item.description,
                'author': item.author,
                'show_cover_pic': self.get_show_cover_pic(item),
                'picurl': self.get_picurl(item),
                'content_url': self.get_content_url(item),
                'from_url': item.from_url,
            })
        multi_item_expander = sorted(multi_item_expander, key=lambda k: k.get('id'))
        return multi_item_expander

    def get_datetime(self, obj):
        return time.strftime('%Y-%m-%d %H:%M', obj.datetime.timetuple())

    class Meta:
        model = LibraryNews
        fields = (
            'id', 'msgid', 'title', 'description', 'author', 'show_cover_pic', 'picurl', 'content_url',
            'from_url', 'storage_location', 'multi_item', 'datetime'
        )
        read_only_fields = ('id', 'msgid', 'title', 'description', 'author', 'from_url')


class LibraryNewsDetailSerializer(LibraryNewsListSeriailzer):
    picture = serializers.SerializerMethodField('get_picture')
    content = serializers.SerializerMethodField('get_content')

    def get_picture(self, obj):
        if not obj.picture:
            return None
        else:
            return obj.picture.key

    def get_content(self, obj):
        return obj.content

    def get_multi_item(self, obj):
        multi_item = LibraryNews.manager.get(
            official_account=obj.official_account,
            plugin_iden=obj.plugin_iden,
            root=obj
        )
        multi_item_expander = []
        for item in multi_item:
            multi_item_expander.append({
                'id': item.pk,
                'title': item.title,
                'description': item.description,
                'author': item.author,
                'show_cover_pic': self.get_show_cover_pic(item),
                'picurl': self.get_picurl(item),
                'picture': self.get_picture(item),
                'content_url': self.get_content_url(item),
                'content': self.get_content(item),
                'from_url': item.from_url,
            })
        multi_item_expander = sorted(multi_item_expander, key=lambda k: k.get('id'))
        return multi_item_expander

    class Meta:
        model = LibraryNews
        fields = (
            'id', 'msgid', 'title', 'description', 'author', 'show_cover_pic', 'picurl', 'picture', 'content_url',
            'content', 'from_url', 'storage_location', 'multi_item', 'datetime'
        )
        read_only_fields = ('id', 'msgid', 'title', 'description', 'author', 'from_url')


class LibraryNewsSingleCreate(object):
    def __init__(self, *args, **kwargs):
        self.title = self._transform(kwargs.get('title'))
        self.author = self._transform(kwargs.get('author'))
        self.picture = self._transform(kwargs.get('picture'))
        self.description = self._transform(kwargs.get('description'))
        self.pattern = kwargs.get('pattern')
        self.content = self._transform(kwargs.get('content'))
        self.url = self._transform(kwargs.get('url'))
        self.from_url = self._transform(kwargs.get('from_url'))

    def _transform(self, value):
        if not value:
            return None
        else:
            return value


class LibraryNewsCreate(object):
    def __init__(self, *args, **kwargs):
        self.news_id = kwargs.get('news_id')  # 如果传入 news_id，则说明需要将原图文 news_id 替换为新图文
        self.official_account = kwargs.get('official_account')
        self.news_array = kwargs.get('news_array')

    def save(self, **kwargs):
        # 初始化当前公众号实例
        official_account = OfficialAccount.objects.get(pk=self.official_account)
        # 如果可用模拟登陆, 则初始化模拟登陆类
        simulation = None
        if official_account.simulation_available:
            wechat_basic = WechatBasic()
            wechat_basic.parse_data(data="""<xml><ToUserName><![CDATA[toUser]]></ToUserName><FromUserName><![CDATA[fromUser]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[this is a test]]></Content><MsgId>1234567890123456</MsgId></xml>""")
            if official_account.has_token_cookies:  # 当已经存在缓存的 token 和 cookies 时直接利用它们初始化
                token_cookies_dict = official_account.get_cache_token_cookies()
                wechat_ext = WechatExt(
                    username=official_account.username,
                    password=official_account.password,
                    token=token_cookies_dict['token'],
                    cookies=token_cookies_dict['cookies'],
                )
                simulation = Simulation(
                    official_account=official_account,
                    wechat_basic=wechat_basic,
                    wechat_ext=wechat_ext
                )
            else:  # 当不存在缓存的 token 和 cookies 时利用用户名密码初始化
                simulation = Simulation(
                    official_account=official_account,
                    wechat_basic=wechat_basic,
                    username=official_account.username,
                    password=official_account.password,
                )

        news = []
        for item in self.news_array:
            if item.pattern == 'text':
                news.append({
                    'title': item.title,
                    'author': item.author,
                    'picture': None if not item.picture else Media.manager.get(item.picture),
                    'description': item.description,
                    'content': item.content,
                    'from_url': item.from_url,
                })
            else:
                news.append({
                    'title': item.title,
                    'author': item.author,
                    'picture': None if not item.picture else Media.manager.get(item.picture),
                    'description': item.description,
                    'url': item.url,
                    'from_url': item.from_url,
                })

        if self.news_id:  # 如果是修改图文，执行修改操作
            root = LibraryNews.manager.modify(pk=self.news_id, news=news)
        else:  # 否则直接插入新图文
            root = LibraryNews.manager.add_mix(
                official_account=official_account,
                plugin_iden='news',
                news=news
            )
        news_list = LibraryNews.manager.get(official_account=official_account, plugin_iden='news', root=root)
        for item in news_list:
            item.update_picurl()  # 更新图片访问地址
            if item.content:
                item.update_url()  # 更新URL地址
            # if official_account.simulation_available:
            #     item.update_picture_id(simulation=simulation)  # 更新图片在远程素材库中的ID
        return news_list


class LibraryNewsSingleCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, error_messages={
        'required': u'图文标题不能为空',
        'invalid': u'输入数据不合法',
    })
    author = serializers.CharField(max_length=100, required=False, error_messages={
        'invalid': u'输入数据不合法',
    })
    picture = serializers.CharField(max_length=40, required=False, error_messages={
        'invalid': u'输入数据不合法',
    })
    description = serializers.CharField(required=False, error_messages={
        'invalid': u'输入数据不合法',
    })
    pattern = serializers.CharField(error_messages={
        'required': u'必须提供图文显示方式',
        'invalid': u'输入数据不合法',
    })
    content = serializers.CharField(required=False, error_messages={
        'invalid': u'输入数据不合法',
    })
    url = serializers.CharField(max_length=1024, required=False, error_messages={
        'invalid': u'输入数据不合法',
    })
    from_url = serializers.CharField(max_length=1024, required=False, error_messages={
        'invalid': u'输入数据不合法',
    })

    def validate_pattern(self, attrs, source):
        pattern = attrs.get(source)
        if pattern not in ['text', 'url']:
            raise serializers.ValidationError(u'参数值非法')
        return attrs

    def validate_content(self, attrs, source):
        content = attrs.get(source)
        if attrs.get('pattern') == 'text' and not content:
            raise serializers.ValidationError(u'图文内容不能为空')
        return attrs

    def validate_url(self, attrs, source):
        url = attrs.get(source)
        if attrs.get('pattern') == 'url' and not url:
            raise serializers.ValidationError(u'跳转地址不能为空')
        return attrs

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            instance.author = attrs.get('author', instance.author)
            instance.picture = attrs.get('picture', instance.picture)
            instance.description = attrs.get('description', instance.description)
            instance.pattern = attrs.get('pattern', instance.pattern)
            instance.content = attrs.get('content', instance.content)
            instance.url = attrs.get('url', instance.url)
            instance.from_url = attrs.get('from_url', instance.from_url)
            return instance
        return LibraryNewsSingleCreate(**attrs)


class LibraryNewsCreateSerializer(serializers.Serializer):
    news_id = serializers.IntegerField(error_messages={
        'invalid': u'输入数据不合法',
    }, required=False)
    official_account = serializers.IntegerField(error_messages={
        'required': u'必须提供公众号',
        'invalid': u'输入数据不合法',
    })
    news_array = LibraryNewsSingleCreateSerializer(many=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.news_id = attrs.get('news_id', instance.news_id)
            instance.official_account = attrs.get('official_account', instance.official_account)
            instance.news_array = attrs.get('news_array', instance.news_array)
            return instance
        return LibraryNewsCreate(**attrs)
