# -*- coding: utf-8 -*-

import HTMLParser

from django.db import models
from django.core.urlresolvers import reverse

from system.official_account.models import OfficialAccount
from system.official_account.utils import OfficialAccountException, OfficialAccountIncorrect, OfficialAccountIncomplete
from system.simulation import Simulation, SimulationException
from system.media.models import Media
from system.rule_match.models import RuleMatch
from system.library.news.exceptions import LibraryNewsException


class LibraryNewsManager(models.Manager):
    """
    素材库 - 图文库 Manager
    """
    def add_remote(self, official_account, plugin_iden, news):
        """
        新建一个完整的远程图文信息
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param news: 一个 list 对象, 每个元素为一个 dict 对象, key 包括 'title', 'description', 'picurl',
                     'url', 'picture', 对应 value 解释见 LibraryNews Model, 除 'title' 外所有 key 值均为可选
        :return: 第一条图文的实例 (LibraryNews)
        """
        parent = None
        first_instance = None
        for item in news:
            tmp = super(LibraryNewsManager, self).create(
                official_account=official_account,
                plugin_iden=plugin_iden,
                parent=parent,
                title=item.get('title'),
                description=item.get('description'),
                picurl=item.get('picurl'),
                url=item.get('url'),
                picture=item.get('picture'),
            )
            if not first_instance:
                first_instance = tmp
            parent = tmp
        return first_instance

    def add_local(self, official_account, plugin_iden, news):
        """
        新建一个完整的本地图文信息
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param news: 一个 list 对象, 每个元素为一个 dict 对象, key 包括 'msgid', 'title', 'description', 'picture',
                    'author', 'content', 'picid', 'from_url', 对应 value 解释见 LibraryNews Model,
                    除 'title', 'content' 外所有 key 值均为可选
        :return: 第一条图文的实例 (LibraryNews)
        """
        parent = None
        first_instance = None
        for item in news:
            tmp = super(LibraryNewsManager, self).create(
                official_account=official_account,
                plugin_iden=plugin_iden,
                parent=parent,
                msgid=item.get('msgid', 0),
                title=item.get('title'),
                description=item.get('description'),
                picture=item.get('picture'),
                author=item.get('author'),
                content=item.get('content'),
                picid=item.get('picid', 0),
                from_url=item.get('from_url'),
            )
            if not first_instance:
                first_instance = tmp
            parent = tmp
        return first_instance

    def add_mix(self, official_account, plugin_iden, news):
        """
        新建一个完整的混合图文信息 (包括文本显示和链接跳转)
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param news: 一个 list 对象, 每个元素为一个 dict 对象, key 包括 'msgid', 'title', 'description', 'picture', 'picurl',
                     'url', 'author', 'content', 'picid', 'from_url', 对应 value 解释见 LibraryNews Model, 除 'title' 外
                     所有 key 值均为可选
        :return: 第一条图文的实例 (LibraryNews)
        """
        parent = None
        first_instance = None
        for item in news:
            tmp = super(LibraryNewsManager, self).create(
                official_account=official_account,
                plugin_iden=plugin_iden,
                parent=parent,
                msgid=item.get('msgid', 0),
                title=item.get('title'),
                description=item.get('description'),
                picture=item.get('picture'),
                picurl=item.get('picurl'),
                url=item.get('url'),
                author=item.get('author'),
                content=item.get('content'),
                picid=item.get('picid', 0),
                from_url=item.get('from_url'),
            )
            if not first_instance:
                first_instance = tmp
            parent = tmp
        return first_instance

    def get(self, official_account, plugin_iden, root):
        """
        获取以 root 为父节点的所有图文回复 (链式)
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param root: 父节点实例 (LibraryNews)
        :return: 一个 list 对象, 一次为所有的图文回复 (以 root 为根, 呈链状)
        """
        if root.plugin_iden != plugin_iden:
            return []
        children = self._get_without_root(official_account=official_account, plugin_iden=plugin_iden, root=root)
        if not children:
            return [root]
        else:
            return [root] + children

    def get_list(self, official_account):
        """
        获取 official_account 公众号下的所有根图文回复节点
        :param official_account: 所属公众号 (OfficialAccount)
        :return: QuerySet 对象, 为所有根图文回复节点的集合
        """
        return super(LibraryNewsManager, self).get_queryset().filter(official_account=official_account).filter(parent=None)

    def modify(self, pk, news):
        """
        修改一个完整的多图文信息
        :param pk: 需要修改的多图文根 ID
        :param news: 一个 list 对象, 每个元素为一个 dict 对象, key 包括 'msgid', 'title', 'description', 'picture', 'picurl',
                     'url', 'author', 'content', 'picid', 'from_url', 对应 value 解释见 LibraryNews Model, 除 'title' 外
                     所有 key 值均为可选
        :return: 修改好的第一条图文的实例 (LibraryNews)
        """
        origin_root = super(LibraryNewsManager, self).get_queryset().get(pk=pk)
        origin_id = origin_root.pk

        # 在原图文素材库中新建新的修改后的图文
        now_root = self.add_mix(
            official_account=origin_root.official_account,
            plugin_iden=origin_root.plugin_iden,
            news=news
        )
        now_id = now_root.pk
        # 在微信回复匹配表中找到原来的reply_id并全部更新为新的ID
        rule_matches = RuleMatch.manager.get_news(news_id=origin_id)
        if rule_matches.exists():
            rule_matches.update(reply_id=now_id)
        # 完成历史使命，将原图文全部删除
        origin_root.delete()  # 删除根时会自动删除相关联的子图文

        return now_root

    def delete(self, pk):
        """
        删除主键以 pk 为根的多图文
        :param pk: 多图文根 ID
        """
        super(LibraryNewsManager, self).get_queryset().get(pk=pk).delete()

    def sync(self, official_account, news):
        """
        与官方管理平台图文素材库同步
        :param official_account: OfficialAccount 实例
        :param news: 列表, 每个元素为一个 LibraryNews 实例
        :return: 官方管理平台中的 msgid
        """
        html_parser = HTMLParser.HTMLParser()

        try:
            simulation = official_account.get_simulation_instance()
        except OfficialAccountException as e:
            raise LibraryNewsException(e)

        for item in news:
            item.update_picurl()  # 更新图片访问地址
            if item.content:
                item.update_url()  # 更新URL地址
            if official_account.simulation_available:
                item.update_picture_id(simulation=simulation)  # 更新图片在远程素材库中的ID

        msgid = None
        # 向微信公众平台素材库中添加该图文信息
        news_dealt = []
        for item in news:
            news_dealt.append({
                'title': item.title,
                'author': item.author,
                'summary': item.description,
                'content': item.content,
                'picture_id': item.picid,
                'from_url': item.from_url,
            })
            for x in news_dealt[-1]:  # 将所有非 picid 的空字段转换为空字符串
                if x != 'picture_id' and not news_dealt[-1][x]:
                    news_dealt[-1][x] = ''
        try:
            simulation.add_news(news=news_dealt)
            # 获取素材库中的图文列表并得到刚才添加的图文的 msgid
            news_list = simulation.get_news_list(page=0)
            for news_single in news_list:
                is_match = True
                for item in news_single['multi_item']:
                    index = item['seq']
                    item['title'] = html_parser.unescape(item['title'])
                    item['author'] = html_parser.unescape(item['author'])
                    item['digest'] = html_parser.unescape(item['digest'])
                    item['source_url'] = html_parser.unescape(item['source_url'])
                    if item['title'] != news_dealt[index]['title'] or item['author'] != news_dealt[index]['author'] or \
                        item['digest'] != news_dealt[index]['summary'] or item['file_id'] != news_dealt[index]['picture_id'] or \
                        item['source_url'] != news_dealt[index]['from_url']:
                        is_match = False
                        break
                if is_match:
                    msgid = news_single['app_id']
                    break
        except SimulationException, e:
            raise LibraryNewsException(e)

        first_news = news[0]
        first_news.msgid = msgid
        first_news.save()
        return msgid

    def _get_without_root(self, official_account, plugin_iden, root):
        """
        获取以 root 为父节点的所有图文回复 (链式), 注意获取到的列表不含 root 在内
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param root: 父节点实例 (LibraryNews)
        :return: 一个 list 对象, 一次为所有的图文回复 (以 root 为根, 呈链状但不含 root)
        """
        now = super(LibraryNewsManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).filter(
            parent=root
        )
        if not now:
            return None

        child = self._get_without_root(official_account=official_account, plugin_iden=plugin_iden, root=now[0])
        if not child:
            return [now[0]]
        else:
            return [now[0]] + child


class LibraryNews(models.Model):
    """
    素材库 - 图文库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)

    parent = models.ForeignKey('self', verbose_name=u'本地/远程-父ID', blank=True, null=True)
    title = models.CharField(u'本地/远程-图文标题', max_length=100)
    description = models.TextField(u'本地/远程-图文描述', blank=True, null=True)
    picture = models.ForeignKey(Media, related_name='+', verbose_name=u'本地/远程-图片存储地址', blank=True, null=True, on_delete=models.SET_NULL)

    picurl = models.CharField(u'远程-缩略图图片地址', max_length=1024, blank=True, null=True)
    url = models.CharField(u'远程-跳转地址', max_length=1024, blank=True, null=True)

    msgid = models.BigIntegerField(u'本地-公众平台图文ID号', default=0)
    author = models.CharField(u'本地-图文作者', max_length=100, blank=True, null=True)
    content = models.TextField(u'本地-图文内容', blank=True, null=True)
    picid = models.IntegerField(u'本地-素材库中的图片ID', default=0)
    from_url = models.CharField(u'本地-来源URL', max_length=1024, blank=True, null=True)
    view_count = models.IntegerField(u'本地-图文访问次数', default=0)
    vote_count = models.IntegerField(u'本地-图文点赞数目', default=0)
    datetime = models.DateTimeField(u'本地-图文新建日期', auto_now_add=True)

    objects = models.Manager()
    manager = LibraryNewsManager()

    class Meta:
        verbose_name = u'素材库 - 图文库'
        verbose_name_plural = u'素材库 - 图文库'
        db_table = 'library_news'

    def __unicode__(self):
        return self.title

    def is_simulated(self):
        """
        检测当前图文是否可以以模拟登陆方式发送给用户
        :return: 如果可以返回 True
        """
        if self.title and self.content:
            return True
        return False

    def is_basic(self):
        """
        检测当前图文是否可以以普通方式发送给用户
        :return: 如果可以返回 True
        """
        if self.title:
            return True
        return False

    def add_view_count(self, count=1):
        """
        增加当前图文访问量
        :param count: 需要增加的数目
        """
        self.view_count += count
        self.save()
        return self.view_count

    def add_vote_count(self, count=1):
        """
        增加当前图文点赞数
        :param count: 需要增加的个数
        """
        self.vote_count += count
        self.save()
        return self.vote_count

    def update_picture_id(self, simulation):
        """
        由 picture 更新 picid
        :param simulation: 模拟登陆实例 (Simulation)
        """
        if not self.picture:  # 当本地没有存储图片时, 清空 picid
            self.picid = 0
            self.save()
            return self.picid

        try:
            fid = simulation.upload_file(filepath=self.picture.media.path)
            self.picid = int(fid)
        except SimulationException:  # 出现模拟登录错误时放弃上传
            self.picid = 0
        self.save()
        return self.picid

    def update_picurl(self):
        """
        由 picture 更新 picurl
        """
        if not self.picture:
            self.picurl = None
        else:
            self.picurl = reverse('filetranslator:download', kwargs={'key': self.picture.pk})
        self.save()
        return self.picurl

    def update_url(self, url=None):
        """
        由 content 更新 url

        注意当存在 content 时会强制令 url 为图文浏览页面 url, 如果需要更新 url, 请删除 content 中的内容
        :param url: 指定 url, 默认为不指定
        """
        if not self.content:
            self.url = url
        else:
            self.url = reverse('news:detail', kwargs={'pk': self.pk})
        self.save()
        return self.url