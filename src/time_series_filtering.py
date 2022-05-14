from abc import ABC, abstractmethod
from collections import deque

import numpy as np


class BaseTimeSeriesFilter(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class IdenticalTimeSeriesFilter(BaseTimeSeriesFilter):
    def __call__(self, data):
        return data


class MovingAverageFilter(BaseTimeSeriesFilter):
    def __init__(self, filter_window_size):
        self.queue = deque(maxlen=filter_window_size)

    def __call__(self, data):
        self.queue.append(data)
        return np.mean(self.queue, axis=0)


class ExponentialMovingAverageFilter(BaseTimeSeriesFilter):
    def __init__(self, alpha):
        if not (0 < alpha < 1):
            print('Parameter alpha should be in range (0, 1)')
            exit(-1)

        self.alpha = alpha
        self.prev = None

    def __call__(self, data, alpha=None):
        if alpha is not None:
            self.alpha = alpha

        self.prev = data if self.prev is None else \
            self.alpha * data + (1 - self.alpha) * self.prev
        return self.prev


class OneEuroFilter(BaseTimeSeriesFilter):
    """
    https://cristal.univ-lille.fr/~casiez/1euro/
    """
    def __init__(self, data_frequency, min_cutoff_frequency=1.0, beta=0.0, derivative_cutoff_frequency=1.0):
        for argument, argument_name in ((data_frequency, 'data_frequency'),
                                        (min_cutoff_frequency, 'min_cutoff_frequency'),
                                        (derivative_cutoff_frequency, 'derivative_cutoff_frequency')):
            self.check_is_positive(argument, argument_name)

        self.data_frequency = data_frequency
        self.min_cutoff_frequency = min_cutoff_frequency
        self.beta = beta
        self.derivative_cutoff_frequency = derivative_cutoff_frequency
        self.data_low_pass_filter = ExponentialMovingAverageFilter(self.get_alpha(self.min_cutoff_frequency))
        self.derivative_low_pass_filter = ExponentialMovingAverageFilter(
            self.get_alpha(self.derivative_cutoff_frequency))
        self.prev_data = None
        self.prev_timestamp = None

    def get_alpha(self, cutoff_frequency):
        te = 1 / self.data_frequency
        tau = 1 / (2 * np.pi * cutoff_frequency)
        return 1 / (1 + tau / te)

    def __call__(self, data, timestamp=None):
        if self.prev_timestamp and timestamp:
            self.data_frequency = 1 / (timestamp - self.prev_timestamp)
        derivative = 0.0 if self.prev_data is None else (data - self.prev_data) * self.data_frequency

        self.prev_data = data
        self.prev_timestamp = timestamp

        derivative_estimation = self.derivative_low_pass_filter(derivative,
                                                                alpha=self.get_alpha(self.derivative_cutoff_frequency))
        # use it to update the cutoff frequency
        cutoff_frequency = self.min_cutoff_frequency + self.beta * np.abs(derivative_estimation)
        # filter the given value
        return self.data_low_pass_filter(data, alpha=self.get_alpha(cutoff_frequency))

    @staticmethod
    def check_is_positive(argument, argument_name):
        if argument <= 0:
            print(f'{argument_name} should be >0, got {argument}')
            exit(-1)
