class Grammar(object):
    def __init__(self):
        self.INHIBITED_CONNECTION = 0x7F

    def get_part_of_speech_size(self):
        pass

    def get_part_of_speech_string(self, pos_id):
        pass

    def get_part_of_speech_id(self, pos):
        pass

    def get_connect_cost(self, left_id, right_id, cost=None):
        pass

    def get_bos_parameter(self):
        pass

    def get_eos_parameter(self):
        pass

    def get_character_category(self):
        pass

    def set_character_category(self, char_category):
        pass
