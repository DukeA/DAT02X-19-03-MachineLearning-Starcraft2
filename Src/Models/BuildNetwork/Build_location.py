from Models.BuildNetwork.Building_size import Builiding_size


class Build_location:

    def get_good_locations(self, lists):
        if len(lists) <= 0:
            return lists
        build_location = []
        position_start_barracks = 82 * Builiding_size.Barracks_size.value
        position_start_supply = 82 * Builiding_size.supply_depot_size.value
        for i in lists:
            build_location.append(Build_location.get_surronding_area(self, lists, position_start_barracks + i))
            build_location.append(Build_location.get_surronding_area(self, lists, position_start_supply + i))
        return build_location

    def get_surronding_area(self, lists, building_location):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        for i in Build_location.step_range(
                self, Build_location.get_location_in_list(self, building_location % 82, building_location % 82) - 82
                , Build_location.get_location_in_list(self, building_location % 82, building_location % 82), 82):
            if lists[i] == 0:
                x_max += 1
        for i in Build_location.step_range(
                self, Build_location.get_location_in_list(self, building_location % 82, building_location % 82)
                , Build_location.get_location_in_list(self, building_location % 82, building_location % 82) + 82, 82):
            if lists[i] == 0:
                x_min += 1
        for i in Build_location.step_range(
                self, Build_location.get_location_in_list(self, building_location % 82, building_location % 82)
                , Build_location.get_location_in_list(self, building_location % 82, building_location % 82) + 82, 1):
            if lists[i] == 0:
                y_max += 1
        for i in Build_location.step_range(
                self, Build_location.get_location_in_list(self, building_location % 82, building_location % 82) - 82
                , Build_location.get_location_in_list(self, building_location % 82, building_location % 82), 1):
            if lists[i] == 0:
                y_min += 1
        return (x_min, x_max, y_min.y_max, building_location)

    def step_range(self, start, end, step):
        while start <= end:
            yield start
            start += step

    def get_location_in_list(self, start, value):
        return start * 82 + value
