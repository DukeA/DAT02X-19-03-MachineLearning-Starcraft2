import keras
import tensorflow as tf
#from Models.BotFile.State import State
class ImitationAgent:
    def __init__(self):
        super(ImitationAgent, self).__init__()
    #model = keras.models.load_model("Overfitted50accuracy")
    model = tf.keras.models.load_model("C:/Users/Claes/Desktop/TestModels/Overfitted50accuracy.h5", compile=True)

    def predict(self, game_state):
        normalized_game_state = game_state.get_normalized_game_state()
        index = 0
        prediction = self.model.predict(normalized_game_state)[0]
        for i in len(prediction):
            if prediction[i] == 1:
                index = i

        if index == 0:
            return "attack"
        if index == 1:
            return "build_barracks"
        if index == 2:
            return "build_factory"
        if index == 3:
            return "build_hellion"
        if index == 4:
            return "build_marine"
        if index == 5:
            return "build_medivac"
        if index == 6:
            return "build_reaper"
        if index == 7:
            return "build_refinery"
        if index == 8:
            return "build_scv"
        if index == 9:
            return "build_starport"
        if index == 10:
            return "build_supply_depot"
        if index == 11:
            return "build_viking"
        if index == 12:
            return "expand"
        if index == 13:
            return "no_op"
        if index == 14:
            return "retreat"
        if index == 15:
            return "return_scv"

        return "no_op"

