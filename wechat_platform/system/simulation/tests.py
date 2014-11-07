# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.simulation.models import SimulationMatch


class SimulationTest(WechatTestCase):
    def test_simulation(self):
        #official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')
        #wechat_basic = WechatBasic()
        #wechat_basic.parse_data(data=self.make_raw_text_message(time='1415035839', content=u'今天'))
        pass

    def test_simulation_match(self):
        """
        测试模拟登陆关系匹配
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')
        match_1 = SimulationMatch.manager.add(
            official_account=official_account,
            openid='openid123',
            fakeid='fakeid321',
        )
        match_2 = SimulationMatch.manager.add(
            official_account=official_account,
            openid='myopenid',
            fakeid='myfakeid',
        )
        self.assertEqual(2, SimulationMatch.objects.count())
        self.assertEqual(match_1.official_account, official_account)
        self.assertEqual(match_1.openid, 'openid123')
        self.assertEqual(match_1.fakeid, 'fakeid321')
        self.assertEqual(match_2.official_account, official_account)
        self.assertEqual(match_2.openid, 'myopenid')
        self.assertEqual(match_2.fakeid, 'myfakeid')

        self.assertEqual(SimulationMatch.manager.get(official_account=official_account, openid='openid123'), match_1)
        self.assertEqual(SimulationMatch.manager.get(official_account=official_account, fakeid='myfakeid'), match_2)
        self.assertEqual(SimulationMatch.manager.get(official_account=official_account, openid='openid123', fakeid='fakeid321'), match_1)