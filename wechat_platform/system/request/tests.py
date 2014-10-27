# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic

from system.core.test import WechatTestCase
from system.request.models import RequestMessage


class RequestTest(WechatTestCase):
    def test_add_text_request(self):
        """
        测试添加文本消息请求
        """
        self.assertEqual(0, RequestMessage.objects.count())

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_text_message()
        request = RequestMessage.manager.add_text(msgid=msgid, target=target, source=source, time=time, raw=raw,
                                                  content=u'测试文本消息')
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
        request = RequestMessage.manager.add(wechat_instance)
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
        self.assertEqual(0, RequestMessage.objects.count())

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_image_message()
        picurl = self.make_url()
        request = RequestMessage.manager.add_image(msgid=msgid, target=target, source=source, time=time, raw=raw, picurl=picurl)
        self.assertEqual(request.msgid, msgid)
        self.assertEqual(request.target, target)
        self.assertEqual(request.source, source)
        self.assertEqual(request.time, time)
        self.assertEqual(request.raw, raw)
        self.assertEqual(request.image_picurl, picurl)

        self.assertEqual(1, RequestMessage.objects.count())