
OUTPUT_DIR = "output/mazes"
LOG_DIR = "output/logs"

DIFFICULTY_SETTINGS = {
    "easy": {"grid_size": 21},
    "medium": {"grid_size": 31},
    "hard": {"grid_size": 41},
    "very_hard": {"grid_size": 61},
    "extreme": {"grid_size": 81},
}
# Note: odd grid sizes ensure corridors at odd indices, simplifying edge openings.
