from game.map.road_sections.static_road_section import StaticRoadSection
from game.map.road_sections.dynamic_road_section import DynamicRoadSection
from game.map.road_sections.border_section import BorderRoadSection
from game.map.road_sections.base_road_section import BaseRoadSection
from game.map.road_section_manager import RoadSectionManager
from game.map.road_sections.moving_direction import MovingDirection


def read_road_section(
    data: dict, road_section_manager: RoadSectionManager
) -> BaseRoadSection:
    if data["type"] == "DynamicRoadSection":
        return DynamicRoadSection(
            index=data["index"],
            road_section_manager=road_section_manager,
            car_speed=data["car_speed"],
            car_direction=MovingDirection(data["car_direction"]),
            car_starting_positions=data["car_starting_positions"],
            border_overhang=data["border_overhang"],
            previous_section=None,
        )
    elif data["type"] == "StaticRoadSection":
        return StaticRoadSection(
            index=data["index"],
            road_section_manager=road_section_manager,
            static_obstacle_positions=data["static_obstacle_positions"],
            previous_section=None,
        )
    elif data["type"] == "BorderRoadSection":
        return BorderRoadSection(
            index=data["index"],
            road_section_manager=road_section_manager,
            previous_section=None,
        )
    else:
        raise ValueError(f"Unknown road section type {data['type']}")
