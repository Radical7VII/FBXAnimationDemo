# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from mod_log import logger
from mod.common.minecraftEnum import KeyBoardType

from player_gac import Player
from action_mgr import PlayerActionManager as ActionMgr

ClientSystem = clientApi.GetClientSystemCls()


class AnimModelClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.listen_events()
        self.action_mgr = ActionMgr(self)
        self.player_id = clientApi.GetLocalPlayerId()
        self.player_data = {}
        self.model_id = None
        self.model_name = 'player_base'

    def listen_events(self):
        name_space = clientApi.GetEngineNamespace()
        system_name = clientApi.GetEngineSystemName()
        event_list = [
            ('UiInitFinished', self.ui_init_finished),
            ('OnKeyPressInGame', self.on_key_press),
            # ('ClientJumpButtonPressDownEvent', self.jump_start),
            # ('LeftClickBeforeClientEvent', self.click),
            # ('LeftClickReleaseClientEvent', self.release)
        ]
        for event_name, handler in event_list:
            self.ListenForEvent(name_space, system_name, event_name, self, handler)

    def Update(self):
        pass

    def ui_init_finished(self, args):
        pass

    def on_key_press(self, args):
        """调试用"""
        key = args['key']
        is_down = args['isDown']
        if is_down == '1':
            pass

    def get_playing_list(self):
        """获取当前动画列表"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        playing_anim_list = comp.GetPlayingAnimList(self.model_id)
        return playing_anim_list
