# Demonstration for Mr. Gopi after our discussion on 2020-06-13
# Used PEP8 convention as much as possible
# Had issues with static variables and hence the redeclaration of lat_range and long_range in two difference places

from json import load
from statistics import mean
from textwrap import wrap
from math import pi
from typing import List


class GeoHash:
    def __init__(self, hash_type: int = 32):
        self.geo_hash_dict = load(open(f'geohash_alphabet_{hash_type}ghs.json', 'r'))
        self.geo_hash_dict_reverse = [
            {str(y): x for x, y in self.geo_hash_dict[0].items()},
            {y: x for x, y in self.geo_hash_dict[1].items()}
        ]

        self.hash_type = hash_type

        self.bit_wrap = 5
        if hash_type == 64:
            self.bit_wrap = 6

        self.bit_wrap = {
            32: 5,
            64: 6,
            256: 8
        }

        self.hash_wrap = {
            32: 1,
            64: 1,
            256: 2
        }

    @staticmethod
    def binary_to_number(lat_long_code, lat_long_range):
        for i in lat_long_code:
            if i == '0':
                lat_long_range[1] = mean(lat_long_range)
            elif i == '1':
                lat_long_range[0] = mean(lat_long_range)
        return mean(lat_long_range)

    def geo_hash_to_lat_long(self, geo_hash_string: str) -> [float, float]:
        lat_range = [-90, 90]
        long_range = [-180, 180]

        lat_long_string = "".join([self.geo_hash_dict[1][str(self.geo_hash_dict[0][i])] for i in
                                   wrap(geo_hash_string, self.hash_wrap[self.hash_type])])
        [long_code, lat_code] = [lat_long_string[x::2] for x in range(2)]
        return [self.binary_to_number(lat_code, lat_range), self.binary_to_number(long_code, long_range)]

    def geo_hash_to_lat_long_theta_phi(self, geo_hash_string: str, split_type: int = 4) -> List[float]:
        long_range = [-180, 180]
        lat_range = [-90, 90]
        theta_range = [-2 * pi, 2 * pi]
        phi_range = [-pi, pi]

        param_ranges = [lat_range, long_range, theta_range, phi_range]
        param_ranges = param_ranges[:split_type]
        lat_long_string = "".join([self.geo_hash_dict[1][str(self.geo_hash_dict[0][i])] for i in
                                   wrap(geo_hash_string, self.hash_wrap[self.hash_type])])
        param_codes = [lat_long_string[x::split_type] for x in range(split_type)]

        return [self.binary_to_number(param_code, param_range) for param_code, param_range in
                zip(param_codes, param_ranges)]

    # def geo_hash_to_lat_long(self, geo_hash_string: str) -> List[float]:
    #     return self.geo_hash_to_lat_long_theta_phi(geo_hash_string=geo_hash_string, split_type=2)

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

    def lat_long_to_geo_hash(self, lat, long, precision: int = 8) -> str:
        lat_range = [-90, 90]
        long_range = [-180, 180]
        lat_code = self.hash_encoder(lat, lat_range, self.bit_wrap[self.hash_type] * precision)
        long_code = self.hash_encoder(long, long_range, self.bit_wrap[self.hash_type] * precision)
        # noinspection PyTypeChecker
        binaries = wrap(''.join([val for pair in zip(long_code, lat_code) for val in pair]),
                        self.bit_wrap[self.hash_type])
        geo_hash_out = ''
        for binary in binaries:
            geo_hash_out = geo_hash_out + self.geo_hash_dict_reverse[0][self.geo_hash_dict_reverse[1][binary]]
        return geo_hash_out

    def lat_long_theta_phi_to_geo_hash(self, lat, long, theta, phi, precision: int = 8) -> str:
        lat_range = [-90, 90]
        long_range = [-180, 180]
        theta_range = [-2 * pi, 2 * pi]
        phi_range = [-pi, pi]

        param_args = [long, lat, theta, phi]
        param_ranges = [long_range, lat_range, theta_range, phi_range]

        lat_code = self.hash_encoder(lat, lat_range, self.bit_wrap[self.hash_type] * precision)
        long_code = self.hash_encoder(long, long_range, self.bit_wrap[self.hash_type] * precision)

        param_codes = [self.hash_encoder(x, y, self.bit_wrap[self.hash_type] * precision) for x, y in
                       zip(param_args, param_ranges)]

        # noinspection PyTypeChecker
        binaries = wrap(''.join([val for pair in zip(param_codes) for val in pair]),
                        self.bit_wrap[self.hash_type])

        geo_hash_out = "".join(
            [self.geo_hash_dict_reverse[0][self.geo_hash_dict_reverse[1][binary]] for binary in binaries])

        return geo_hash_out


def decimal_to_geo_hash(self):
    pass


if __name__ == '__main__':
    for hash_kind in [32, 64, 256]:
        print(f"Hash type : {hash_kind}ghs")
        geo_hash = GeoHash(hash_type=hash_kind)
        lat_long_pair = [42.605, -5.603]
        calculated_hash = geo_hash.lat_long_to_geo_hash(lat_long_pair[0], lat_long_pair[1])
        print(f"Calculated hash for Lat-Long of {lat_long_pair} is {calculated_hash}")
        print(f"Recalculated Lat-Long from the above hash are {geo_hash.geo_hash_to_lat_long(calculated_hash)}")
        if hash_kind == 256:
            print("\nQuartet Notation")
            # quartet = [-22.49621710041538, 149.11290143150836, 4.815615568277845, -0.6845378023414236]
            quartet = [0, 0, 0, 0]
            calculated_hash = geo_hash.lat_long_theta_phi_to_geo_hash(quartet[0], quartet[1], quartet[2], quartet[3])
            print(f"Calculated hash for Lat-Long of {quartet} is {calculated_hash}")
            print(
                f"Recalculated Lat-Long from the above hash are {geo_hash.geo_hash_to_lat_long_theta_phi(calculated_hash)}")
        print()
