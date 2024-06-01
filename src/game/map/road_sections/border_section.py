from __future__ import annotations
from typing import TYPE_CHECKING
from .static_road_section import StaticRoadSection
from .base_road_section import BaseRoadSection

if TYPE_CHECKING:
    from game.map.road_section_manager import RoadSectionManager
    from game.player.player import Player


class BorderRoadSection(StaticRoadSection):
    def __init__(
        self,
        index: int,
        road_section_manager: RoadSectionManager,
        previous_section: BaseRoadSection = None,
    ) -> None:
        super().__init__(
            index=index,
            road_section_manager=road_section_manager,
            previous_section=previous_section,
            static_obstacle_positions=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )

    def get_obstacle_positions_relative_to_player(self, player) -> list[float]:
        return [0, 1.0, -0.8125, 0.8125]

    def to_dict(self):
        return {
            "type": "BorderRoadSection",
            "index": self.index,
            "static_obstacle_positions": self.static_obstacle_positions,
        }
