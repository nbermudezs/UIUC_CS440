# Inspired by the Java implementation described here:
# http://csclab.murraystate.edu/~bob.pilgrim/445/munkres.html
# and the definition of the method found in:
# https://www.math.ucdavis.edu/~saito/data/emd/munkres.pdf

import copy
from enum import Enum

class MunkresStep(Enum):
    SUBSTRACT_MINIMAS = 1
    DRAW_COVER_LINES = 2
    CHECK_OPTIMALITY = 3
    COVER_UNCOVERED_ZEROS = 4
    FIND_ALTERNATIVE_COVER = 5
    AUGMENT_MATRIX = 6
    DONE = 7

class MarkOperation(Enum):
    UNMARK = 0
    STAR = 1
    PRIME = 2

class Munkres:
    def __init__(self):
        self.steps = {}
        self.steps[ MunkresStep.SUBSTRACT_MINIMAS ] = self.step1
        self.steps[ MunkresStep.DRAW_COVER_LINES ] = self.step2
        self.steps[ MunkresStep.CHECK_OPTIMALITY ] = self.step3
        self.steps[ MunkresStep.COVER_UNCOVERED_ZEROS ] = self.step4
        self.steps[ MunkresStep.FIND_ALTERNATIVE_COVER ] = self.step5
        self.steps[ MunkresStep.AUGMENT_MATRIX ] = self.step6

    def compute(self, original_matrix):
        self.n = len(original_matrix)
        self.matrix = copy.deepcopy(original_matrix)
        self.range_n = range(self.n)

        # for line covering
        self.row_covered = [ False for _ in self.range_n ]
        self.col_covered = [ False for _ in self.range_n ]

        # create a 2D array to keep track of the candidates
        self.marked = [ [ MarkOperation.UNMARK for i in self.range_n ] for j in self.range_n ]

        # path for changing line coverage
        # 2D array of nx2 dimensions. column 1 = row, column 2 = column of the matrix
        self.recover_path = [ [ 0 for i in range(self.n * 2) ] for j in range(self.n * 2) ]

        step = MunkresStep.SUBSTRACT_MINIMAS
        while step != MunkresStep.DONE:
            step = self.steps[ step ]()

        # get me the result!
        assignment = []
        for row in range(self.n):
            for col in range(self.n):
                if self.marked[ row ][ col ] == MarkOperation.STAR:
                    assignment.append((row, col))
        return assignment

    def step1(self):
        # col_minimas = {}
        for row in self.range_n:
            # get minima
            minval = min(self.matrix[ row ])
            # update row values
            for col in self.range_n:
                self.matrix[ row ][ col ] -= minval
                # col_minimas[ col ] = min(col_minimas.get(col, float('inf')), self.matrix[ row ][ col ])

        # # substract col minimas
        # for row in self.range_n:
        #     for col in self.range_n:
        #         self.matrix[ row ][ col ] -= col_minimas[ col ]

        return MunkresStep.DRAW_COVER_LINES

    def step2(self):
        for row in self.range_n:
            for col in self.range_n:
                if (self.matrix[ row ][ col ] == 0) and (not self.col_covered[ col ]) and (not self.row_covered[ row ]):
                    self.marked[ row ][ col ] = MarkOperation.STAR
                    self.col_covered[ col ] = True
                    self.row_covered[ row ] = True
                    break
        self.reset_covered_arrays()
        return MunkresStep.CHECK_OPTIMALITY

    def step3(self):
        count = 0
        for row in self.range_n:
            for col in self.range_n:
                if self.marked[ row ][ col ] == MarkOperation.STAR and not self.col_covered[ col ]:
                    self.col_covered[ col ] = True
                    count += 1

        if count == self.n:
            return MunkresStep.DONE
        else:
            return MunkresStep.COVER_UNCOVERED_ZEROS

    def step4(self):
        current_row = 0
        current_col = 0
        while True:
            zero_position = self.find_uncovered_zero(current_row, current_col)
            current_row = zero_position[ 0 ]
            current_col = zero_position[ 1 ]
            if current_row == -1:
                # all zeros are covered
                return MunkresStep.AUGMENT_MATRIX
            self.marked[ current_row ][ current_col ] = MarkOperation.PRIME
            star_col = self.starred_zero_in_row(current_row)
            if star_col == -1:
                # there was only one zero starred in this row
                self.primed_zero_col = current_col
                self.primed_zero_row = current_row
                return MunkresStep.FIND_ALTERNATIVE_COVER
            else:
                current_col = star_col
                self.row_covered[ current_row ] = True
                self.col_covered[ current_col ] = False

    def step5(self):
        recover_path = self.recover_path
        current_row = self.primed_zero_row
        current_col = self.primed_zero_col

        path_row = 0

        recover_path[ path_row ][ 0 ] = current_row
        recover_path[ path_row ][ 1 ] = current_col

        while True:
            starred_zero_row = self.starred_zero_in_col(recover_path[ path_row ][ 1 ])
            if starred_zero_row == -1:
                break
            path_row += 1
            # keep the same column
            recover_path[ path_row ][ 1 ] = recover_path[ path_row - 1 ][ 1 ]

            # next item in the path is the row we just found
            recover_path[ path_row ][ 0 ] = starred_zero_row

            primed_zero_col = self.primed_zero_in_row(starred_zero_row)
            path_row += 1
            recover_path[ path_row ][ 0 ] = recover_path[ path_row - 1 ][ 0 ]
            recover_path[ path_row ][ 1 ] = primed_zero_col

        for i in range(path_row + 1):
            pos = recover_path[ i ]
            if self.marked[ pos[ 0 ] ][ pos[ 1 ] ] == MarkOperation.STAR:
                self.marked[ pos[ 0 ] ][ pos[ 1 ] ] = MarkOperation.UNMARK
            else:
                self.marked[ pos[ 0 ] ][ pos[ 1 ] ] = MarkOperation.STAR

        for row in self.range_n:
            for col in self.range_n:
                if self.marked[ row ][ col ] == MarkOperation.PRIME:
                    self.marked[ row ][ col ] = MarkOperation.UNMARK

        self.reset_covered_arrays()
        return MunkresStep.CHECK_OPTIMALITY

    def step6(self):
        minimal = self.find_uncovered_smallest()
        for row in self.range_n:
            for col in self.range_n:
                if self.row_covered[ row ]:
                    self.matrix[ row ][ col ] += minimal
                if not self.col_covered[ col ]:
                    self.matrix[ row ][ col ] -= minimal
        return MunkresStep.COVER_UNCOVERED_ZEROS

    def reset_covered_arrays(self):
        for index in self.range_n:
            self.col_covered[ index ] = False
            self.row_covered[ index ] = False

    def starred_zero_in_col(self, col):
        for row in self.range_n:
            if self.marked[ row ][ col ] == MarkOperation.STAR:
                return row
        return -1

    def starred_zero_in_row(self, row):
        for col in self.range_n:
            if self.marked[ row ][ col ] == MarkOperation.STAR:
                return col
        return -1

    def primed_zero_in_row(self, row):
        for col in self.range_n:
            if self.marked[ row ][ col ] == MarkOperation.PRIME:
                return col
        return -1

    def find_uncovered_smallest(self):
        minimal = float('inf')
        for row in self.range_n:
            for col in self.range_n:
                if not self.row_covered[ row ] and not self.col_covered[ col ]:
                    minimal = min(minimal, self.matrix[ row ][ col ])
        return minimal

    def find_uncovered_zero(self, initial_row, initial_col):
        row = initial_row
        while True:
            col = initial_col
            while True:
                if self.matrix[ row ][ col ] == 0 and (not self.row_covered[ row ]) and (not self.col_covered[ col ]):
                    return (row, col)
                col = (col + 1) % self.n
                if col == initial_col:
                    # it already cycled through the columns.
                    # python doesn't have do.while loops *facepalm*
                    break
            row = (row + 1) % self.n
            if row == initial_row:
                break
        # failure :(
        return (-1, -1)
