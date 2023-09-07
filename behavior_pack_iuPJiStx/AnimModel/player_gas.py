import mod.server.extraServerApi as serverApi


class Player(object):
    def __init__(self, player_id):
        self.player_id = None
        self.current_cloth = None
        self.model_id = None

    def get_model(self):
        if not self.current_cloth:
            self.set_model('rabbit')
            return

    def set_model(self, model_name):
        comp = serverApi.GetEngineCompFactory().CreateModel(self.player_id)
        self.model_id = comp.SetModel(model_name)
        return self.model_id
