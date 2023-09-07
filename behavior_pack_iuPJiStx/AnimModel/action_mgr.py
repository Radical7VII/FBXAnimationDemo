# coding=utf-8
import weakref
import mod.client.extraClientApi as clientApi
from mod_log import logger
from model_cfg import AnimCfg
from mod.common.minecraftEnum import KeyBoardType


class PlayerActionManager(object):
    def __init__(self, system):
        logger.debug('玩家动作系统')
        self.system = weakref.proxy(system)
        # 基础参数
        self.player_id = clientApi.GetLocalPlayerId()
        self.model_id = None
        # 动画相关
        self.anim_list = []
        self.listen_engine_events()

    def listen_engine_events(self):
        """监听引擎事件"""
        name_space = clientApi.GetEngineNamespace()
        system_name = clientApi.GetEngineSystemName()
        event_list = [
            ('OnScriptTickClient', self.Update),
            ('UiInitFinished', self.ui_init),
            ('WalkAnimBeginClientEvent', self.walking_begin),
            ('WalkAnimEndClientEvent', self.walking_end),
            ('ClientJumpButtonPressDownEvent', self.jump_begin),
            ('OnGroundClientEvent', self.jump_end),
            ('OnKeyPressInGame', self.on_key_press),
        ]
        for event_name, handler in event_list:
            self.system.ListenForEvent(name_space, system_name, event_name, self, handler)

    def ui_init(self, args=None):
        # logger.debug('初始化')
        self.model_id = self.set_model()

    def Update(self):
        self.update_anim_list()

    def on_key_press(self, args):
        """调试用"""
        key = args['key']
        is_down = args['isDown']
        if is_down == '1':
            if key == str(KeyBoardType.KEY_I):
                self.ui_init()

    def set_model(self):
        """将玩家模型设置为鱿鱼"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        m_id = comp.SetModel('player_base')
        return m_id

    def bind_item(self):
        """绑定手持物体"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.BindItemToBone(self.model_id, "hand.r", 0)

    def update_anim_list(self):
        """将该函数放在update下，可以打印出玩家当前播放的动画列表"""
        old_list = self.anim_list
        new_list = self.get_anim_list()
        if old_list == new_list:
            return
        self.anim_list = new_list
        logger.debug(self.anim_list)

    def get_anim_list(self):
        """获取当前动画列表"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        return comp.GetPlayingAnimList(self.model_id)

    def play_anim(self, anim_name, is_loop=True, is_blend=False, layer=0):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.ModelPlayAni(self.model_id, anim_name, is_loop, is_blend, layer)

    def stop_anim(self, anim_name):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.ModelStopAni(self.model_id, anim_name)

    def set_anim_param(self, param_name, value):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        suc = comp.SetAnim1DControlParam(self.model_id, param_name, value)
        self.param_dict[param_name] = value
        # logger.debug(self.param_dict)
        return suc

    # =====================================================================
    def walking_begin(self, args):
        pass

    def walking_end(self, args):
        pass

    def jump_begin(self, args):
        pass

    def jump_end(self, args):
        pass
