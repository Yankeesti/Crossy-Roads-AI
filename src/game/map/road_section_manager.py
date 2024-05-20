import pygame

from game import config
from game.map.road_sections.static_road_section import StaticRoadSection
from game.map.road_sections.base_road_section import BaseRoadSection


class RoadSectionManager:
    def __init__(self):
        super().__init__()
        section_neg_two = StaticRoadSection(index=-2, road_section_manager=self)
        section_neg_one = StaticRoadSection(
            index=-1, road_section_manager=self, previous_section=section_neg_two
        )
        section_neg_two.next_section = section_neg_one
        section_neg_one.previous_section = section_neg_two
        self.road_sections: list[BaseRoadSection] = [StaticRoadSection(index=0, road_section_manager=self,previous_section=section_neg_one)]
        section_neg_one.next_section = self.road_sections[0]

    def generate_sections(self, min_sections_to_generate: int):
        sections_created: int = 0
        while sections_created < min_sections_to_generate:
            new_section = StaticRoadSection(
                index=len(self.road_sections)-1,
                road_section_manager=self,
                previous_section=self.road_sections[-1],
            )
            self.road_sections[-1].next_section = new_section
            self.road_sections.append(new_section)
            sections_created += 1

    def get_sections_to_draw(self, y: int):
        y = int((abs(y) - config.WINDOW_HEIGHT) // config.BLOCK_SIZE)
        return self.get_section(y + 2).get_sections_to_draw()

    def get_section(self, index: int):
        if len(self.road_sections) <= index:
            self.generate_sections(index - len(self.road_sections) + 1)
        return self.road_sections[index]

    def update(self):
        # update the sections
        pass
