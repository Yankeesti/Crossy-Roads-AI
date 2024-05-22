BLOCK_SIZE = 100
ROAD_COLUMNS = 9  # represents the colums that are stepable by the player
DISPLAYED_ROAD_SECTIONS = (
    9  # represents the number of road sections that are displayed on the screen
)
UNSTEPABLEE_COLUMNS = 2  # represents the number of columns on th right and left side of the game that are not stapable by the player
COLUMNS_TOTAL = ROAD_COLUMNS + UNSTEPABLEE_COLUMNS * 2
BORDER_LEFT = BLOCK_SIZE * UNSTEPABLEE_COLUMNS
BORDER_RIGHT = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS)

WINDOW_WIDTH = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS * 2)
WINDOW_HEIGHT = BLOCK_SIZE * DISPLAYED_ROAD_SECTIONS

# Player related
PLAYER_SPEED = 10  # Ticks needed to move 1 Block
MAX_BLOCKS_BACK = 2
INPUT_FETCH_INTERVAL = (
    10  # the interval in wich the Player Fetches the Input from the controller
)
KILLING_POINT_SPEED = 0  # the speed at wich the killing point moves towards the player
PLAYER_PAUSE_AFTER_MOVE = 10  # the amount of frames the player pauses after a move

# Road Section related
MAX_OBSTACLES = (
    3  # the maximum amount of obstacles that can be placed on a road section
)
MAX_CAR_SPEED = 0.075  # the maximum speed of the cars on the road section

DYNAMIC_SECTION_IN_A_ROW = [
    0,
    1,
    2,
    3,
    4,
]  # Lists represents the possible amount of dynamic road sections that are placed in a row
DYNAMIC_SECTION_IN_A_ROW_PROB = [
    0.1,
    0.3,
    0.25,
    0.2,
    0.15,
]  # Lists represents the probability of the amount of dynamic road sections that are placed in a row

STATIC_SECTIONS_IN_A_ROW = [1, 2, 3, 4]
STATIC_SECTIONS_IN_A_ROW_PROB = [0.5, 0.2, 0.15, 0.1, 0.05]

MAX_OVERHANG = 4
