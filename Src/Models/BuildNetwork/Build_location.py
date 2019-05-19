import math
from pysc2.lib import features


class Build_location:
    LIST = []


    """
        :param lists - The value where the location of the points are located.
        The method which takes out the good locations 
        where it is able to build an building 
    """

    def get_good_locations(self, lists,obs, base_location):
        if len(lists) <= 0:
            return lists
        Build_location.LIST = lists
        build_location = []
        list = Build_location.get_surronding_area(self, Build_location.LIST)
        build_points = Build_location().build_location(list,obs, base_location)
        return build_points


    """
        :param lists -The building list with all the coordinates for the map
        :param building_location- The starting location for the pixel point of the screen
        The algorithm  takes the points and uses the area of histograms to calculate the largest area sizes, 
        from that it can then calculate out the largest  area.
    """

    def get_surronding_area(self, lists):
        build_areas = []
        done = False
        Row = len(lists)
        Column = len(lists[0])
        while done == False:
            max_area = 0
            area = 0
            high_value = 0
            length = 0
            current_length = 0
            State = lists
            width = 0
            height = 0
            x_pos = 0
            y_pos = 0
            x_tmp_max_pos = 0
            for i in range(0, Row):
                for j in range(0, Column):
                    if lists[i][j] == 1:
                        if i == 0:
                            State[i][j] = 1
                        else:
                            State[i][j] = State[i - 1][j] + 1
                high_value = max(State[i])
                for y in range(3, high_value + 1):
                    current_length = 0
                    length = 0
                    for x in range(0, Column):
                        list_value = State[x]
                        if State[i][x] >= y:
                            current_length += 1
                        else:
                            current_length = 0
                        if current_length > length:
                            length = current_length
                            x_tmp_max_pos = x
                    area = length * y
                    if area >= max_area:
                        height = y
                        y_pos = i
                        x_pos = x_tmp_max_pos
                        width = length
                        max_area = area
            if  width >=3 and height >=3:
                build_areas.append((x_pos, y_pos, width, height))
            else:
                return build_areas

            for i in range(x_pos, x_pos - width, -1):
                for j in range(y_pos, y_pos - height, -1):
                    lists[j][i] = 0

            for i in range(0, len(lists)):
                if max(lists[i]) == 0:
                    done = True
                else:
                    done = False
                    break

        return build_areas

    """
        :param The list of locations where to build the location can be built
            The method takes the location and gives back the middle build_location and
            the reward of building there.
    """

    def build_location(self, list,obs, base_location):
        value = any((0 in i) for i in list)
        empty_tuple = any(i == () for i in list)
        if len(list) <= 0 or value or empty_tuple:
            return []
        build_location = []
        build_location_reward =[]
        for i in list:
            area_position = i
            x_pos = math.ceil(area_position[0] - (area_position[2] / 2))
            y_pos = math.ceil(area_position[1] - (area_position[3] / 2))
            reward = int(area_position[2] * area_position[3])
            start_y, start_x = obs.observation.camera_position
            if start_x < 128 and start_y < 128:
                if  base_location[0]< x_pos  or base_location[1] < y_pos :
                    build_location.append([x_pos, y_pos])
                    build_location_reward.append(reward)
            elif start_x > 128 and start_y > 128:
                if base_location[0] > x_pos  or base_location[1] > y_pos :
                    build_location.append([x_pos, y_pos])
                    build_location_reward.append(reward)

        return build_location, build_location_reward
