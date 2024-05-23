import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import game
from game.map.road_sections.road_section_reader import read_road_section
import json


def generate_starting_road_sections(
    amount_of_games: int,
    starting_road_sections: int,
    file_path: str = "src/neat_training/road_sections.json",
):
    """ "Generates the map for the given amount of games and stores it in the road_section json file."""
    data = []
    for i in range(amount_of_games):
        manager = game.map.road_section_manager.RoadSectionManager()
        manager.generate_sections(starting_road_sections)
        data.append(manager.to_dict())
    with open(file_path, "w") as file:
        json.dump(data, file)


class NeatRoadSectionManager(game.map.road_section_manager.RoadSectionManager):
    """This Class is responsible for managing the road sections in the NEAT training.
    it takes its roadsections from the json file,
    when the generate sections Method is called it will create new road sections, store them in the roadsection json file


    This is needed so all Geoms can train on exactly the same road sections."""

    def __init__(
        self, index: int = 0, file_path: str = "src/neat_training/road_sections.json"
    ):
        self.road_sections = []
        with open(file_path, "r") as file:
            self.complete_data = json.load(file)
        self.data = self.complete_data[index]
        self.index = index
        self.init_sections()
        self.generated_sections = False
        self.file_path = file_path

    def init_sections(self):
        """Initializes the road sections with the data from the json file."""
        self.road_sections = []
        section_neg_three = read_road_section(self.data[0], self)
        section_neg_two = read_road_section(self.data[1], self)
        section_neg_one = read_road_section(self.data[2], self)
        section_neg_three.next_section = section_neg_two
        section_neg_two.previous_section = section_neg_three
        section_neg_two.next_section = section_neg_one
        section_neg_one.previous_section = section_neg_two
        self.road_sections.append(read_road_section(self.data[3], self))
        section_neg_one.next_section = self.road_sections[0]
        self.road_sections[0].previous_section = section_neg_one

        for i in range(4, len(self.data)):
            section = read_road_section(self.data[i], self)
            self.road_sections[-1].next_section = section
            section.previous_section = self.road_sections[-1]
            self.road_sections.append(section)

    def generate_sections(self, min_sections_to_generate: int):
        super().generate_sections(10)
        # Store newly generated Sections in File
        self.complete_data[self.index] = self.to_dict()
        with open(self.file_path, "w") as file:
            json.dump(self.complete_data, file)
        self.generated_sections = True

    def set_index(self, index: int):
        self.__init__(index)
