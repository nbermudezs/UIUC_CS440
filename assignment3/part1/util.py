class Util:
    def print_matrix(matrix, rows, cols):
        import math, sys
        format = '%s'

        for i in range(rows):
            sep = '['
            for j in range(cols):
                val = matrix[ i ][ j ]
                formatted = (format % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')
