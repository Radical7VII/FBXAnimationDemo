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
        self.blend_value = 0  # 混合值，0是idle，1是walk
        self.animation_stack = ["idle"]
        self.anim_blend_values = {
            'idle_walk': {
                'blend_value': 0.0
            },
            'walk_jump': {
                'blend_value': 0.0
            },
            'idle_jump': {
                'blend_value': 0.0
            }
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
        # logger.debug('初始化')
        self.model_id = self.set_model()
        self.init_anim()

    def init_anim(self):
        # 同一时间，两个动画都在后台进行播放
        # anim_list结果是 ['idle', 'walk']
        self.register_anim_param('idle', 'walk', 'idle_walk')
        self.register_anim_param('walk', 'jump', 'walk_jump')
        self.register_anim_param('idle', 'jump', 'idle_jump')
        self.play_anim('idle', True, True)

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

    def register_anim_param(self, anim1, anim2, param_name):
        """注册动画混合"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        comp.RegisterAnim1DControlParam(self.model_id, anim1, anim2, param_name)

    def set_anim_param(self, param_name, value):
        """设置动画混合值"""
        comp = clientApi.GetEngineCompFactory().CreateModel(self.player_id)
        suc = comp.SetAnim1DControlParam(self.model_id, param_name, value)
        return suc

    # =====================================================================
    def walking_begin(self, args):
        self.animation_stack.append('walk')
        self.play_anim('walk', True, True)
        self.update_idle_and_walk_value('+')
        
    def update_idle_and_walk_value(self, operator):
        if operator == '+':
            if self.anim_blend_values['idle_walk']['blend_value'] < 1.0:
                self.anim_blend_values['idle_walk']['blend_value'] += 0.1
            elif self.anim_blend_values['idle_walk']['blend_value'] >= 1.0:
                return
        if operator == '-':
            if self.anim_blend_values['idle_walk']['blend_value'] > 0.1:
                self.anim_blend_values['idle_walk']['blend_value'] -= 0.1
                if self.anim_blend_values['idle_walk']['blend_value'] == 0.0:
                    self.stop_anim('walk')
                    return
        self.set_anim_param('idle_walk', self.anim_blend_values['idle_walk']['blend_value'])
        clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddTimer(0.0,
                                                                                     self.update_idle_and_walk_value,
                                                                                     operator)
    
    def walking_end(self, args):
        self.animation_stack.remove('walk')
        self.update_idle_and_walk_value('-')

    def jump_begin(self, args):
        if 'jump' not in self.animation_stack:
            self.animation_stack.append('jump')
        self.play_anim('jump', True, True)
        prev_anim = self.animation_stack[-2]
        def update_blend_value():
            self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'] += 0.1
            if self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'] >= 1.0:
                return
            self.set_anim_param('{}_jump'.format(prev_anim), self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'])
            clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddTimer(0.0, update_blend_value)
        
        update_blend_value()
        
    def jump_end(self, args):
        prev_anim = self.animation_stack[-2]
        if 'jump' in self.animation_stack:
            self.animation_stack.remove('jump')
        def update_blend_value():
            self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'] -= 0.1
            if self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'] <= 0.0:
                self.stop_anim('jump')
                return
            self.set_anim_param('{}_jump'.format(prev_anim), self.anim_blend_values['{}_jump'.format(prev_anim)]['blend_value'])
            clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddTimer(0.0, update_blend_value)
        
        update_blend_value()
