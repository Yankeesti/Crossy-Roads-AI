BLOCK_SIZE = 100
ROAD_COLUMNS = 9 #represents the colums that are stepable by the player
DISPLAYED_ROAD_SECTIONS = 15 #represents the number of road sections that are displayed on the screen
UNSTEPABLEE_COLUMNS = 2 #represents the number of columns on th right and left side of the game that are not stapable by the player

WINDOW_WIDTH = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS * 2)
WINDOW_HEIGHT = BLOCK_SIZE * DISPLAYED_ROAD_SECTIONS

#Player related
PLAYER_SPEED = 10  # Ticks needed to move 1 Block
MAX_BLOCKS_BACK = 2
INPUT_FETCH_INTERVAL = 10 #the interval in wich the Player Fetches the Input from the controller
KILLING_POINT_SPEED = 0.005 #the speed at wich the killing point moves towards the player