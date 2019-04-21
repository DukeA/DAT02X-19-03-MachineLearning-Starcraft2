import math


class Build_location:
    LIST = []

    """
        :param lists - The lists of the points in the environment
        An method which  separates out the values of where the 
    """

    def get_good_points(self, list):
        if len(list) <= 0:
            return list
        point_list = []
        n_list = list
        for points in n_list:
            value_x = points[0]
            value_y = points[1]
            if value_x != -1 and value_x != 81:
                if value_y != -1 and value_y != 81:
                    point_list.append(points)
        return point_list

    """
        :param lists - The value where the location of the points are located.
        The method which takes out the good locations 
        where it is able to build an building 
    """

    def get_good_locations(self, lists):
        if len(lists) <= 0:
            return lists
        Build_location.LIST = lists
        build_location = []
        list = Build_location.get_surronding_area(self, Build_location.LIST)
        performed_build_location = Build_location().get_good_points(build_location)
        list_locations = Build_location().get_build_areas(performed_build_location)
        build_points = Build_location().build_location(list_locations)
        return performed_build_location

    """
        :param lists - The lists of the building points
         The method should take all the values of the point and create an area where it is best to build
    """

    def get_build_areas(self, list):
        if len(list) <= 0:
            return [(0, 0, 0)]
        n_list = list
        builid_location = []
        for i in list:
            start_location = i[2] - i[0]
            end_location = i[2] - i[1]
            builid_location.append(start_location, end_location, i[2])
        return builid_location

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
            y_tmp_max_pos = 0
            for i in range(1, Row):
                for j in range(0, Column):
                    if lists[i][j] == 1:
                        State[i][j] = State[i - 1][j] + 1
                high_value = max(State[i])
                for x in range(3, high_value + 1):
                    for y in range(0, Column):
                        if State[i][y] >= x:
                            current_length += 1
                        else:
                            current_length = 0
                        if current_length > length:
                            length = current_length
                            y_tmp_max_pos = y
                    area = length * x
                    if area >= max_area:
                        width = x
                        x_pos = i
                        y_pos = y_tmp_max_pos
                        height = length
                        max_area = area
                    length = 0

            build_areas.append([x_pos, y_pos, width, height])

            for i in range(x_pos, x_pos - width, -1):
                for j in range(y_pos, y_pos - height, -1):
                    lists[i][j] = 0

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

    def build_location(self, list):
        value = any((0 in i) for i in list)
        empty_tuple = any(i == () for i in list)
        if len(list) <= 0 or value or empty_tuple:
            return []
        build_location = []
        for i in list:
            area_position = i
            x_pos = math.ceil(area_position[0] - (area_position[2] / 2))
            y_pos = math.ceil(area_position[1] - (area_position[3] / 2))
            reward = int(area_position[2] * area_position[3])
            build_location.append((x_pos, y_pos, reward))
        return build_location
