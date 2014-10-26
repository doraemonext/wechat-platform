# -*- coding: utf-8 -*-

from django.test import Client

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount


class ListenTest(WechatTestCase):
    def test_invalid_official_account(self):
        """
        测试非法公众号识别码
        """
        response = self.client.post('/listen/?iden=invalididen')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid IDEN Parameter')

    def test_invalid_verify_parameter(self):
        """
        测试非法微信请求参数
        """
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_1)
        response = self.client.post('/listen/?iden={iden}&signature=a&nonce=b&timestamp=c'.format(iden=official_account.iden))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid Verify Parameter')

    def test_invalid_xml_data(self):
        """
        测试非法XML请求
        """
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_2)
        signature, timestamp, nonce = self.make_verify_parameter(token=official_account.token)
        response = self.client.post('/listen/?iden={iden}&signature={signature}&timestamp={timestamp}&nonce={nonce}'.format(
            iden=official_account.iden,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        ), 'invalid xml', 'text/xml', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid XML Data')