__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'

import math

class ProbabilityDistribution:
    def __init__(self, smoothing = 1):
        self.counts = {}
        self.total_count = 0
        self.smoothing = smoothing

    def add(self, feature):
        count = self.counts.get(feature, 0)
        count += 1
        self.total_count += 1
        self.counts[ feature ] = count

    def laplacian_smoothing(self, feature):
        if feature not in self.counts:
            self.counts[ feature ] = self.smoothing
            self.total_count += self.smoothing

    def get(self, feature):
        self.laplacian_smoothing(feature)
        return self.counts[ feature ]

    def p_of(self, feature):
        return self.get(feature) / self.total_count

    def log_p_of(self, feature):
        return math.log(self.p_of(feature))
