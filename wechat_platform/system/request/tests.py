# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.request import RequestRepeatException
from system.request.models import RequestMessage, RequestEvent


class RequestTest(WechatTestCase):
    def test_repeat_request_message(self):
        """
        测试重复消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestMessage.objects.count())
        wechat_instance_1 = WechatBasic()
        wechat_instance_1.parse_data(data=self.make_raw_text_message())
        request_1 = RequestMessage.manager.add(official_account=official_account, wechat_instance=wechat_instance_1)
        self.assertEqual(1, RequestMessage.objects.count())
        wechat_instance_2 = WechatBasic()
        wechat_instance_2.parse_data(data=self.make_raw_text_message(msgid=request_1.msgid))

        # 检测is_repeat函数
        self.assertTrue(RequestMessage.manager.is_repeat(official_account=official_account, wechat_instance=wechat_instance_2))
        # 检测触发异常
        with self.assertRaises(RequestRepeatException):
            RequestMessage.manager.add(official_account=official_account, wechat_instance=wechat_instance_2)

    def test_repeat_request_event(self):
        """
        测试重复事件请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestEvent.objects.count())
        wechat_instance_1 = WechatBasic()
        wechat_instance_1.parse_data(data=self.make_raw_event_subscribe_message())
        request_1 = RequestEvent.manager.add(official_account=official_account, wechat_instance=wechat_instance_1)
        self.assertEqual(1, RequestEvent.objects.count())
        wechat_instance_2 = WechatBasic()
        wechat_instance_2.parse_data(data=self.make_raw_event_subscribe_message(source=request_1.source, time=request_1.time))

        # 检测is_repeat函数
        self.assertTrue(RequestEvent.manager.is_repeat(official_account=official_account, wechat_instance=wechat_instance_2))
        # 检测触发异常
        with self.assertRaises(RequestRepeatException):
            RequestEvent.manager.add(official_account=official_account, wechat_instance=wechat_instance_2)

    def test_add_text_request(self):
        """
        测试添加文本消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestMessage.objects.count())

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_text_message()
        request = RequestMessage.manager.add_text(official_account=official_account, msgid=msgid, target=target,
                                                  source=source, time=time, raw=raw, content=u'测试文本消息')
        self.assertEqual(request.official_account, official_account)
        self.assertEqual(request.msgid, msgid)
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw, raw)
        self.assertEqual(request.text_content, u'测试文本消息')

        self.assertEqual(1, RequestMessage.objects.count())

    def test_add_text_request_with_wechat_instance(self):
        """
        测试通过wechat实例添加文本消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestMessage.objects.count())

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_text_message(
            msgid=msgid,
            target=target,
            source=source,
            time=time,
            content=u'测试文本消息'
        )
        wechat_instance = WechatBasic()
        wechat_instance.parse_data(raw)
        request = RequestMessage.manager.add(official_account=official_account, wechat_instance=wechat_instance)
        self.assertEqual(request.official_account, official_account)
        self.assertEqual(request.msgid, msgid)
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw.decode('utf-8'), raw)
        self.assertEqual(request.text_content, u'测试文本消息')

        self.assertEqual(1, RequestMessage.objects.count())

    def test_add_image_request(self):
        """
        测试添加图片消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestMessage.objects.count())

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_image_message()
        picurl = self.make_url()
        request = RequestMessage.manager.add_image(official_account=official_account, msgid=msgid, target=target,
                                                   source=source, time=time, raw=raw, picurl=picurl)
        self.assertEqual(request.official_account, official_account)
        self.assertEqual(request.msgid, msgid)
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw, raw)
        self.assertEqual(request.image_picurl, picurl)

        self.assertEqual(1, RequestMessage.objects.count())

    def test_add_event_subscribe_request(self):
        """
        测试添加订阅消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestEvent.objects.count())

        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_event_subscribe_message()
        request = RequestEvent.manager.add_subscribe(official_account=official_account, target=target, source=source, time=time, raw=raw)
        self.assertEqual(request.official_account, official_account)
        self.assertEqual(request.type, 'subscribe')
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw, raw)

        self.assertEqual(1, RequestEvent.objects.count())

    def test_add_event_unsubscribe_request(self):
        """
        测试添加取消订阅消息请求
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        self.assertEqual(0, RequestEvent.objects.count())

        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_event_unsubscribe_message()
        request = RequestEvent.manager.add_unsubscribe(official_account=official_account, target=target, source=source, time=time, raw=raw)
        self.assertEqual(request.official_account, official_account)
        self.assertEqual(request.type, 'unsubscribe')
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw, raw)

        self.assertEqual(1, RequestEvent.objects.count())