# coding=utf-8
import mod.client.extraClientApi as clientApi
from mod_log import logger
import model_cfg


class Player(object):
    # 客户端代码
    def __init__(self, player_id):
        self.player_id = player_id
        self.model_id = None

    def Tick(self):
        pass

    def ui_finished(self):
        pass
