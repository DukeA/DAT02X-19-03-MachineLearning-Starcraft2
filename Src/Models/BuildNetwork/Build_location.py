from Models.BuildNetwork.Building_size import Builiding_size


class Build_location:

    def get_good_locations(self, lists):
        if len(lists) <= 0:
            return lists
        build_location = []
        for i in range(len(lists)):
            build_location.append(Build_location.get_surronding_area(self, lists, i))
        performed_build_location = Build_location.get_good_locations(self, build_location)
        return performed_build_location

    def get_surronding_area(self, lists, building_location):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        value = Build_location().get_location_in_list_by_id(self,building_location)
        step = 1
        done = False
        while done == False:
            for x in range(value[0] - step, value[0] + step, 1):
                if x >= 0 and x <= 81:
                    for y in range(value[1] - step, value[1] + step, 1):
                        if y >= 0 and y <= 81:
                            position = Build_location().get_location_in_list_by_2D(self, x, y)
                            if lists[position] == 1:
                                if x == 0 and x < value[0]:
                                    x_min = -step
                                elif x == 0 and x > value[0]:
                                    x_max = step
                                if y == 0 and y < value[0]:
                                    y_min = -step
                                elif y == 0 and y > value[1]:
                                    y_max = step
                            if lists[position] == 0:
                                done = True
        step += 1
        return (x_min, x_max, y_min, y_max, building_location)

    def get_good_points(self, list):
        if len(list) <= 0:
            return list
        point_list = []
        n_list = list
        for points in n_list:
            if (points[0] != 0 and points[2] != 0) or (points[1] != 0 and points[3] != 0):
                point_list.append(self, points)
        return point_list


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
