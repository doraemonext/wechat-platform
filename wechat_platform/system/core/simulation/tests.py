# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic, WechatExt

from system.official_account.models import OfficialAccount
from system.core.test import WechatTestCase
from system.core.simulation import Simulation


class SimulationTest(WechatTestCase):
    def test_simulation(self):
        #official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')
        #wechat_basic = WechatBasic()
        #wechat_basic.parse_data(data=self.make_raw_text_message(time='1415035839', content=u'今天'))
        pass