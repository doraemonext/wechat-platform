# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

from system.official_account.models import OfficialAccount
from system.simulation import Simulation, SimulationException
from system.media.models import Media


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
                picture_id=item.get('picid', 0),
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