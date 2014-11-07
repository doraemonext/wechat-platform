# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.response.models import Response


class ResponseTest(WechatTestCase):
    def test_add_message_response(self):
        """
        测试添加响应消息
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        msgid = self.make_msgid()
        target = self.make_target()
        source = self.make_source()
        raw = self.make_raw_text_message(
            msgid=msgid,
            target=target,
            source=source,
            content=u'测试文本消息'
        )
        wechat_instance = WechatBasic()
        wechat_instance.parse_data(raw)
        response = Response.manager.add(
            official_account=official_account,
            wechat_instance=wechat_instance,
            type=Response.TYPE_TEXT,
            pattern=Response.PATTERN_SIMULATION,
            raw='test raw content',
            plugin_dict={
                'iden': 'text',
                'reply_id': 1,
            }
        )
        self.assertEqual(response.official_account, official_account)
        self.assertEqual(response.msgid, msgid)
        self.assertEqual(response.target, source)
        self.assertEqual(response.source, target)
        self.assertEqual(response.type, Response.TYPE_TEXT)
        self.assertEqual(response.pattern, Response.PATTERN_SIMULATION)
        self.assertEqual(response.raw, 'test raw content')
        self.assertEqual(response.plugin_iden, 'text')
        self.assertEqual(response.reply_id, 1)

    def test_add_event_response(self):
        """
        测试添加响应事件
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        target = self.make_target()
        source = self.make_source()
        time = self.make_time()
        raw = self.make_raw_event_subscribe_message(
            target=target,
            source=source,
            time=time
        )
        wechat_instance = WechatBasic()
        wechat_instance.parse_data(raw)
        response = Response.manager.add(
            official_account=official_account,
            wechat_instance=wechat_instance,
            type=Response.TYPE_MUSIC,
            pattern=Response.PATTERN_SERVICE,
            raw='test raw',
            plugin_dict={
                'iden': 'text',
                'reply_id': 2,
            }
        )
        self.assertEqual(response.official_account, official_account)
        self.assertEqual(response.msgid, target + str(time))
        self.assertEqual(response.target, source)
        self.assertEqual(response.source, target)
        self.assertEqual(response.type, Response.TYPE_MUSIC)
        self.assertEqual(response.pattern, Response.PATTERN_SERVICE)
        self.assertEqual(response.raw, 'test raw')
        self.assertEqual(response.plugin_iden, 'text')
        self.assertEqual(response.reply_id, 2)

    def test_filter_response(self):
        """
        测试响应消息筛选
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        msgid = self.make_msgid()
        time = self.make_time()

        wechat_instance_1 = WechatBasic()
        wechat_instance_1.parse_data(data=self.make_raw_text_message(msgid=msgid, time=time, content='same content'))
        wechat_instance_2 = WechatBasic()
        wechat_instance_2.parse_data(data=self.make_raw_text_message(msgid=msgid, time=time+5, content='same content'))
        wechat_instance_3 = WechatBasic()
        wechat_instance_3.parse_data(data=self.make_raw_text_message(msgid=msgid, time=time+10, content='same content'))

        response_1 = Response.manager.add(
            official_account=official_account,
            wechat_instance=wechat_instance_1,
            type=Response.TYPE_MUSIC,
            pattern=Response.PATTERN_SIMULATION,
            raw='some random stuff',
            plugin_dict={
                'iden': 'image',
                'reply_id': 5,
            }
        )
        response_2 = Response.manager.add(
            official_account=official_account,
            wechat_instance=wechat_instance_2,
            type=Response.TYPE_TEXT,
            pattern=Response.PATTERN_SIMULATION,
            raw='some random stuff strange',
            plugin_dict={
                'iden': 'image',
                'reply_id': 5,
            }
        )
        response_3 = Response.manager.add(
            official_account=official_account,
            wechat_instance=wechat_instance_3,
            type=Response.TYPE_IMAGE,
            pattern=Response.PATTERN_SIMULATION,
            raw='http://www.google.com/',
            plugin_dict={
                'iden': 'image',
                'reply_id': 5,
            }
        )
        result = Response.manager.get(official_account=official_account, msgid=msgid).order_by('time')
        self.assertEqual(result.count(), 3)
        self.assertEqual(result[0], response_1)
        self.assertEqual(result[1], response_2)
        self.assertEqual(result[2], response_3)