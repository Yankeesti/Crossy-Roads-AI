from game import config
def normalize_signed_input(value: float, min_value: float, max_value: float) -> float:
    """ "normalize input value between -1 and 1"""
    return (value - min_value) / (max_value - min_value) * 2 - 1


def normalize_positive_input(value: float, min_value: float, max_value: float) -> float:
    """Normalize a value that can only be positive to the range 0 to 1."""
    normalized_value = (value - min_value) / (max_value - min_value)
    return normalized_value


def transform_distance(distance: float, max_distance: float = config.MAX_DISTANCE_TO_PLAYER) -> float:
    """Transform distance so that the distance nearest to 0 gets the value far away from 0"""
    if distance < 0:
        return -max_distance - distance
    return max_distance - distance
