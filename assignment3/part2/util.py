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

    def print_as_string(matrix, rows, cols):
        result = ''
        for row in matrix:
            result += ''.join(row) + '\n'
        print(result)

    def print_confusion_matrix(matrix, rows, cols):
        import math, sys
        format = '%5s'

        sep = '[   |'
        for i in sorted(matrix.keys()):
            formatted = (format % i)
            sys.stdout.write(sep + formatted)
            sep = '| '
        sys.stdout.write(']\n')

        for i in sorted(matrix.keys()):
            row_sum = sum(matrix.get(i, {}).values())
            sep = '[ ' + str(i) + ' |'
            for j in sorted(matrix.keys()):
                val = matrix.get(i, {}).get(j, 0) / row_sum * 100.0
                formatted = ('%5.1f' % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')
