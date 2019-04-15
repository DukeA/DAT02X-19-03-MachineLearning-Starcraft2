from Models.BuildNetwork.Building_size import Builiding_size


class Build_location:
    def get_good_points(self, list):
        if len(list) <= 0:
            return list
        point_list = []
        n_list = list
        for points in n_list:
            value_x = points[0]
            value_y = points[1]
            if (value_x != 81 and value_x != 1):
                if (value_y != 81 and value_y != 1):
                    point_list.append(points)
        return point_list

    def get_good_locations(self, lists):
        if len(lists) <= 0:
            return lists
        build_location = []
        values_in_list = len(lists)
        for i in Build_location().step_range(0, values_in_list - 1, 3):
            if lists[i] != 1:
                build_location.append(Build_location.get_surronding_area(self, lists, i))
        performed_build_location = Build_location().get_good_points(build_location)
        return performed_build_location

    def get_surronding_area(self, lists, building_location):
        x_max = y_max = -1
        next_pos = 3
        done = False
        get_location = Build_location().get_location_in_list_by_id(building_location)
        for x in range(get_location[0], 79, 1):
            for y in range(get_location[1], 79, 1):
                if Build_location().check_square(x, y, lists) == False:
                    continue
                while done == False:
                    if x_max == -1:
                        if x + next_pos > 81:
                            x_max = 81
                        else:
                            for i in range(x, x + next_pos, 1):
                                position = Build_location().get_location_in_list_by_2D(i, y)
                                value_position = lists[position]
                                if lists[position] == 1:
                                    x_max = i
                                    break
                    if y_max == -1:
                        if y + next_pos > 81:
                            y_max = 81
                        else:
                            for j in range(y, y + next_pos, 1):
                                position = Build_location().get_location_in_list_by_2D(x, j)
                                if lists[position] == 1:
                                    y_max = j
                                    break
                    next_pos += 2
                    if x_max != -1 and y_max != -1:
                        done = True
        return (x_max, y_max, building_location)

    def check_square(self, x, y, lists):
        for i in range(x, x + 2, 1):
            for j in range(y, y + 2, 1):
                position = Build_location().get_location_in_list_by_2D(i, j)
                if lists[position] == 1:
                    return False
        return True

    def step_range(self, start, end, step):
        while start <= end:
            yield start
            start += step

    def get_location_in_list_by_id(self, i):
        x = i % 82
        y = int(x / 82)
        return (x, y)

    def get_location_in_list_by_2D(self, value_x, value_y):
        return value_x * 82 + value_y
