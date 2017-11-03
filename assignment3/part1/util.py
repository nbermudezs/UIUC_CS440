__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

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

    def print_confusion_matrix(matrix, rows, cols):
        import math, sys
        format = '%5.2f'

        sep = '[   |'
        for i in range(rows):
            formatted = ('%5d' % i)
            sys.stdout.write(sep + formatted)
            sep = '| '
        sys.stdout.write(']\n')

        for i in range(rows):
            row_sum = sum(matrix.get(i, {}).values())
            sep = '[ ' + str(i) + ' |'
            for j in range(cols):
                val = matrix.get(i, {}).get(j, 0) / row_sum * 100.0
                formatted = (format % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')
