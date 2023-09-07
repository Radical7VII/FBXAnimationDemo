# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from mod_log import logger

ServerSystem = serverApi.GetServerSystemCls()


class AnimModelServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.listen_events()
        self.player_data = {}
        self.jump_id = None

    def listen_events(self):
        name_space = serverApi.GetEngineNamespace()
        system_name = serverApi.GetEngineSystemName()
        self.ListenForEvent(name_space, system_name, 'AddServerPlayerEvent', self, self.on_add_player)
        self.ListenForEvent(name_space, system_name, 'ServerChatEvent', self, self.on_chat)
        self.ListenForEvent(name_space, system_name, 'ClientLoadAddonsFinishServerEvent', self, self.load_finished)

    def on_add_player(self, args):
        player_id = args['id']

    def load_finished(self, args):
        player_id = args['playerId']

    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def on_chat(self, args):
        player_id = args['playerId']
        message = args['message']
