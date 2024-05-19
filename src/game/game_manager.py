from player.controller import Controller
from player.player_manager import PlayerManager
from map.road_section_manager import RoadSectionManager


class GameManager:

    def __init__(self,controllers : list[Controller],road_section_manager: RoadSectionManager,) -> None:
        self.road_section_manager = road_section_manager
        self.player_manager = PlayerManager(controllers)

    def reset(self,controllers : list[Controller],road_section_manager: RoadSectionManager) -> None:
        pass

    def update(self) -> bool:
        pass