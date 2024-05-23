import pygame
import random

from game import config
from game.map.road_sections.static_road_section import StaticRoadSection
from game.map.road_sections.base_road_section import BaseRoadSection
from game.map.road_sections.border_section import BorderRoadSection
from game.map.road_sections.dynamic_road_section import (
    DynamicRoadSection,
    get_random_car_positions,
)
from game.map.road_sections.moving_direction import MovingDirection


class RoadSectionManager:
    def __init__(self):
        super().__init__()
        section_neg_three = StaticRoadSection(index=-3, road_section_manager=self)
        section_neg_two = StaticRoadSection(
            index=-2, road_section_manager=self, previous_section=section_neg_three
        )
        section_neg_three.next_section = section_neg_two
        section_neg_one = BorderRoadSection(
            index=-1, road_section_manager=self, previous_section=section_neg_two
        )
        section_neg_two.next_section = section_neg_one
        self.road_sections: list[BaseRoadSection] = [
            StaticRoadSection(
                index=0,
                road_section_manager=self,
                previous_section=section_neg_one,
                static_obstacle_positions=[],
            )
        ]
        section_neg_one.next_section = self.road_sections[0]

    def generate_sections(self, min_sections_to_generate: int):
        sections_created: int = 0
        while sections_created < min_sections_to_generate:
            section_group_size = random.choices(
                config.DYNAMIC_SECTION_IN_A_ROW,
                config.DYNAMIC_SECTION_IN_A_ROW_PROB,
                k=1,
            )[0]
            for _ in range(section_group_size):
                self.generate__dynamic_section()
            sections_created += section_group_size
            static_section = StaticRoadSection(
                index=len(self.road_sections),
                road_section_manager=self,
                previous_section=self.road_sections[-1],
            )
            self.road_sections[-1].next_section = static_section
            self.road_sections.append(static_section)

    def generate__dynamic_section(self):
        over_hang = round(random.uniform(0, config.MAX_OVERHANG), 2)
        direction = random.choice([MovingDirection.LEFT, MovingDirection.RIGHT])
        new_section = DynamicRoadSection(
            index=len(self.road_sections),
            road_section_manager=self,
            previous_section=self.road_sections[-1],
            car_speed=round(
                random.uniform(0.3 * config.MAX_CAR_SPEED, config.MAX_CAR_SPEED), 3
            ),
            car_direction=direction,
            car_starting_positions=get_random_car_positions(over_hang, direction),
            border_overhang=over_hang,
        )

        self.road_sections[-1].next_section = new_section
        self.road_sections.append(new_section)

    def get_sections_to_draw(self, y: int):
        y = int((abs(y) - config.WINDOW_HEIGHT) // config.BLOCK_SIZE)
        return self.get_section(y + 2).get_sections_to_draw()

    def get_section(self, index: int):
        if len(self.road_sections) <= index:
            self.generate_sections(index - len(self.road_sections) + 1)
        return self.road_sections[index]

    def update(self):
        for section in self.road_sections:
            section.update()
        pass

    def to_dict(self):
        output = [section.to_dict() for section in self.road_sections]
        output.insert(0, self.road_sections[0].previous_section.to_dict())
        output.insert(
            0, self.road_sections[0].previous_section.previous_section.to_dict()
        )
        output.insert(
            0,
            self.road_sections[
                0
            ].previous_section.previous_section.previous_section.to_dict(),
        )
        return output
