import json


class Config:
    def __init__(self, json_file):
        with open(json_file) as json_data_file:
            self.config_data = json.load(json_data_file)
        self.team_a_name = self.config_data["team_a_name"]
        self.team_b_name = self.config_data["team_b_name"]
        self.team_a_players = self.config_data["team_a_players"]
        self.team_b_players = self.config_data["team_b_players"]
