from typing import List, Tuple, NamedTuple

class XYZPoint(NamedTuple):
    x: int
    y: int
    z: int

GridCorners = Tuple[XYZPoint, XYZPoint, XYZPoint, XYZPoint]

class Grid3D:
    """
    Grid3D is a iterable collection of XYZPoints generated from a set of grid
    corner positions and a number of rows and columns
    """
    def __init__(self, grid_corners: GridCorners, rows: int, columns: int, rowsz: int):
        self.__current_position: int = 0
        self.__positions: List[XYZPoint] = []

        x_start = grid_corners[0][0]
        x_end = grid_corners[1][0]

        y_start = grid_corners[1][1]
        y_end = grid_corners[2][1]

        z_start = grid_corners[2][2]
        z_end = grid_corners[3][2]

        column_step: float = (x_start - x_end) / (columns  - 1)
        row_step: float = (y_start - y_end) / (rows - 1)
        rowsz_step: float = (z_start - z_end) / (rowsz - 1)

        for column in range(columns):
            for row in range(rows):
                for rowsza in range(rowsz):
                    x = x_start - (column_step * column)
                    y = y_start - (row_step * row)
                    z = z_start - (rowsz_step * rowsza) #z = z_end + (rowsz_step * rowsza)
                    self.__positions.append(XYZPoint(x = x, y = y, z = z))


    def __iter__(self):
        return self


    def __next__(self) -> XYZPoint:
        if self.__current_position > len(self.__positions) - 1:
            raise StopIteration
        else:
            next_position = self.__positions[self.__current_position]
            self.__current_position += 1
            return next_position
