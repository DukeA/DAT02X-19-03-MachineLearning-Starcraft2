


class Coordinates():
    BARRACKS_X = 80
    BARRACKS_Y = 40

    # minimap locations. The first tuple is the top-left start location and the second is the bottom-right start.
    # Not entirely accurate (i.e. Command Center isn't centered).
    START_LOCATIONS = [(11.4, 16.8), (51.5, 49.0)]

    # minimap locations, reversed exists to simplify spawning in different corners
    EXPO_LOCATIONS = [(22, 18), (13, 26), (18, 32), (22, 26), (31, 19),
                  (13, 42), (22, 51), (41, 15), (50, 24), (32, 47), (41, 40), (45, 35), (50, 40), (41, 48)]
    # screen_location, reversed exists to simplify spawning in different corners
    CC_LOCATIONS = [(42, 44), (43, 40), (44, 27), (42, 37), (45, 40),
                (36, 37), (46, 36), (37, 42), (47, 41), (38, 38), (41, 41), (39, 40), (40, 38), (41, 34)]
    EXPO_LOCATIONS2 = list(reversed(EXPO_LOCATIONS))
    CC_LOCATIONS2 = list(reversed(CC_LOCATIONS))
