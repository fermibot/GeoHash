# Demonstration for Mr. Gopi after our discussion on 2020-06-13
# Used PEP8 convention as much as possible
# Had issues with static variables and hence the redeclaration of lat_range and long_range in two difference places

from json import load
from statistics import mean
from textwrap import wrap
from math import pi
from typing import List
from random import random


class Geohash:
    def __init__(self, hash_type: int = 32):
        self.geo_hash_dict = load(open(f'geohash_alphabet_{hash_type}ghs.json', 'r'))
        self.geo_hash_dict_reverse = [
            {str(y): x for x, y in self.geo_hash_dict[0].items()},
            {y: x for x, y in self.geo_hash_dict[1].items()}
        ]

        self.hash_type = hash_type

        self.bit_wrap = {
            32: 5,
            64: 6,
            256: 8,
            4096: 12
        }

        self.hash_wrap = {
            32: 1,
            64: 1,
            256: 2,
            4096: 2
        }

        self.split_type = {
            32: 2,
            64: 2,
            256: 4,
            4056: 6
        }

    @staticmethod
    def binary_to_number(lat_long_code, lat_long_range):
        for i in lat_long_code:
            if i == '0':
                lat_long_range[1] = mean(lat_long_range)
            elif i == '1':
                lat_long_range[0] = mean(lat_long_range)
        return mean(lat_long_range)

    def hash_to_nums(self, geo_hash_string: str, split_type: int = 4) -> List[float]:
        long_range = [-180, 180]
        lat_range = [-90, 90]
        theta_range = [-2 * pi, 2 * pi]
        phi_range = [-pi, pi]
        alpha_range = [-10, 10]
        beta_range = [-34, 67]

        param_ranges = (long_range, lat_range, theta_range, phi_range, alpha_range, beta_range)
        param_ranges = param_ranges[:split_type]
        lat_long_string = "".join([self.geo_hash_dict[1][str(self.geo_hash_dict[0][i])] for i in
                                   wrap(geo_hash_string, self.hash_wrap[self.hash_type])])

        param_codes = [lat_long_string[x::split_type] for x in range(split_type)]

        return [self.binary_to_number(param_code, param_range) for param_code, param_range in
                zip(param_codes, param_ranges)]

    @staticmethod
    def hash_encoder(lat_long, lat_long_range, precision) -> int:
        lat_long_code = ''
        for i in range(precision):
            center = mean(lat_long_range)
            if lat_long_range[0] <= lat_long < center:
                lat_long_code = lat_long_code + '0'
                lat_long_range[1] = center
            elif center <= lat_long <= lat_long_range[1]:
                lat_long_code = lat_long_code + '1'
                lat_long_range[0] = center
        return lat_long_code

    def nums_to_geohash(self, nums: list, precision: int = 8) -> str:
        long_range = [-180, 180]
        lat_range = [-90, 90]
        theta_range = [-2 * pi, 2 * pi]
        phi_range = [-pi, pi]
        alpha_range = [-10, 10]
        beta_range = [-34, 67]

        ranges = [long_range, lat_range, theta_range, phi_range, alpha_range, beta_range]
        ranges = ranges[:len(nums)]
        codes = [self.hash_encoder(x, y, self.bit_wrap[self.hash_type] * precision) for x, y in zip(nums, ranges)]
        binaries = wrap(''.join([val for pair in zip(*codes) for val in pair]), self.bit_wrap[self.hash_type])
        geo_hash_out = "".join(
            [self.geo_hash_dict_reverse[0][self.geo_hash_dict_reverse[1][binary]] for binary in binaries])

        return geo_hash_out


if __name__ == '__main__':
    pass
