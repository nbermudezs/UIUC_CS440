__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

from queue import PriorityQueue
import matplotlib.pyplot as plt

class Util:
    def plot_training_curve(data):
        plt.scatter(range(len(data)), data, s=4)
        plt.show()

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

    def print_confusion_matrix(matrix, rows, cols, show_legends = False):
        import math, sys
        format = '%6.2f'

        sep = '[   |'
        for i in range(rows):
            formatted = ('%6d' % i)
            sys.stdout.write(sep + formatted)
            sep = '| '
        sys.stdout.write(']\n')

        for i, key_i in enumerate(sorted(matrix.keys())):
            row_sum = sum(matrix.get(key_i, {}).values())
            sep = '[ ' + str(i) + ' |'
            for j, key_j in enumerate(sorted(matrix.keys())):
                val = matrix.get(key_i, {}).get(key_j, 0) / row_sum * 100.0
                formatted = (format % val)
                sys.stdout.write(sep + formatted)
                sep = ', '
            sys.stdout.write(']\n')

        if show_legends:
            print('Table legends: ', end='')
            keys = sorted(matrix.keys())
            for i, key in enumerate(keys):
                print('class ' + str(i) + '=' + key + '; ', end='')
            print('\n')


    def pick_pairs_for_inspection(confusion_matrix, count = 4):
        queue = PriorityQueue()
        for ref_label, row in confusion_matrix.items():
            for label, value in row.items():
                if ref_label == label:
                    continue
                queue.put((-value, (ref_label, label)))
        result = []
        for i in range(count):
            result.append(queue.get()[ 1 ])
        return result
