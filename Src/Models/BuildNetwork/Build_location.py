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
        The algorithm  takes the points and then add's for the locations which has the highest area free  
        from that it then saves the algorithm into a tuple where it should be located
    """

    def get_surronding_area(self, lists):
        build_areas = []
        done = False
        Row = len(lists)
        Column = len(lists[0])

        State = [[0 for k in range(Column)] for l in range(Row)]

        for i in range(1, Row):
            for j in range(1, Column):
                if lists[i][j] == 1:
                    State[i][j] = min(State[i][j - 1], State[i - 1][j],
                                      State[i - 1][j - 1]) + 1
                else:
                    State[i][j] = 0

        while done == False:
            max_of_s = State[0][0]
            max_i = 0
            max_j = 0
            for i in range(Row):
                for j in range(Column):
                    if (max_of_s <= State[i][j]):
                        max_of_s = State[i][j]
                        max_i = i
                        max_j = j

            build_areas.append([max_i, max_j, max_of_s])

            for i in range(max_i, max_i - max_of_s, -1):
                for j in range(max_j, max_j - max_of_s, -1):
                    State[i][j] = -1


            for i in range(Row):
                if max(State[i]) == 0:
                    done = True
                else:
                    done = False
                    break


        return build_areas
