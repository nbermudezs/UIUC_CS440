__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import matplotlib.pyplot as plt

class Util:
    def plot_training_curve(data):
        plt.scatter(range(len(data)), data, s=4)
        plt.show()
