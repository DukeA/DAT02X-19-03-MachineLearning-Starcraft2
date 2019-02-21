


from Models.BuildOrders.Singleton import Singelton



class ActionSingelton(metaclass=Singelton):

    def __init__(self):
        super(ActionSingelton, self).__init__()
        self.new_action = None


    def get_action(self):
        return self.new_action


    def set_action(self, action):
        self.new_action = action