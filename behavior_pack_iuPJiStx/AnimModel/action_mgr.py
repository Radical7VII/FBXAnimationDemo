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
        self.state = ''
        self.param_dict = {
            'idle_walk': 0,
            'idle_jump': 0,
            'walk_jump': 0,
        }
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
        logger.debug('初始化')
        self.model_id = self.set_model()
        logger.debug(self.model_id)
        self.register_param()
        self.init_all_anim()

    def register_param(self):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.RegisterAnim1DControlParam(self.model_id, 'idle', 'walk', 'idle_walk')
        comp.RegisterAnim1DControlParam(self.model_id, 'idle', 'jump', 'idle_jump')
        comp.RegisterAnim1DControlParam(self.model_id, 'walk', 'jump', 'walk_jump')

    def init_all_anim(self):
        for anim_name in AnimCfg['player_base']:
            cfg = AnimCfg['player_base'][anim_name]
            loop = cfg['loop']
            layer = cfg['layer']
            mask = cfg['mask']
            self.play_anim(anim_name, loop, True)

    def Update(self):
        self.update_anim_list()

    def on_key_press(self, args):
        """调试用"""
        key = args['key']
        is_down = args['isDown']
        if is_down == '1':
            if key == str(KeyBoardType.KEY_I):
                self.ui_init()

    def bind_item(self):
        """绑定手持物体"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.BindItemToBone(self.model_id, "hand.r", 0)

    def update_anim_list(self):
        old_list = self.anim_list
        new_list = self.get_anim_list()
        if old_list == new_list:
            return
        self.anim_list = new_list
        logger.debug(self.anim_list)

    def get_anim_list(self):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        return comp.GetPlayingAnimList(self.model_id)

    def play_anim(self, anim_name, is_loop=True, is_blend=False, layer=0):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.ModelPlayAni(self.model_id, anim_name, is_loop, is_blend, layer)
        self.state = anim_name

    def stop_anim(self, anim_name):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.ModelStopAni(self.model_id, anim_name)

    def play_anim_new(self, anim):
        state = self.state
        print state, anim
        if state == 'idle':
            if anim == 'walk':
                self.set_anim_param('idle_walk', 1)
                self.set_anim_param('idle_jump', 0)
                self.set_anim_param('walk_jump', 0)
            elif anim == 'jump':
                self.set_anim_param('idle_walk', 0)
                self.set_anim_param('idle_jump', 1)
                self.set_anim_param('walk_jump', 0)
        elif state == 'walk':
            if anim == 'idle':
                self.set_anim_param('idle_walk', 0)
                self.set_anim_param('idle_jump', 1)
                self.set_anim_param('walk_jump', 0)
            elif anim == 'jump':
                self.set_anim_param('idle_walk', 0)
                self.set_anim_param('idle_jump', 1)
                self.set_anim_param('walk_jump', 0)
        elif state == 'jump':
            if anim == 'idle':
                self.set_anim_param('idle_walk', 0)
                self.set_anim_param('idle_jump', 1)
                self.set_anim_param('walk_jump', 0)
            elif anim == 'walk':
                self.set_anim_param('idle_walk', 0)
                self.set_anim_param('idle_jump', 1)
                self.set_anim_param('walk_jump', 0)
        self.state = anim

    def set_anim_param(self, param_name, value):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        suc = comp.SetAnim1DControlParam(self.model_id, param_name, value)
        self.param_dict[param_name] = value
        logger.debug(self.param_dict)
        return suc

    def set_model(self):
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        m_id = comp.SetModel('player_base')
        return m_id

    # =====================================================================
    def walking_begin(self, args):
        self.play_anim_new('walk')

    def walking_end(self, args):
        self.play_anim_new('idle')

    def jump_begin(self, args):
        self.play_anim_new('jump')
        pass

    def jump_end(self, args):
        self.play_anim_new(self.state)
