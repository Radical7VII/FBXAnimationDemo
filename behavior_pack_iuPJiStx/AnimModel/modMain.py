# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.mod import Mod


@Mod.Binding(name="AnimModel", version="0.0.1")
class AnimModel(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def AnimModelServerInit(self):
        serverApi.RegisterSystem('AnimModel', 'AnimModelServer',
                                 'AnimModel.AnimModelServerSystem.AnimModelServerSystem')

    @Mod.DestroyServer()
    def AnimModelServerDestroy(self):
        pass

    @Mod.InitClient()
    def AnimModelClientInit(self):
        clientApi.RegisterSystem('AnimModel', 'AnimModelClient',
                                 'AnimModel.AnimModelClientSystem.AnimModelClientSystem')

    @Mod.DestroyClient()
    def AnimModelClientDestroy(self):
        pass
