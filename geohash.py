# Demonstration for Mr. Gopi after our discussion on 2020-06-14
# Used PEP8 convention as much as possible
# Had issues with static variables and hence the redeclaration of lat_range and long_range in two difference places

from json import load
from statistics import mean
from textwrap import wrap


class GeoHash:
    def __init__(self):
        self.geo_hash_dict = load(open('geohash_alphabet.json', 'r'))
        self.geo_hash_dict_reverse = [
            {str(y): x for x, y in self.geo_hash_dict[0].items()},
            {y: x for x, y in self.geo_hash_dict[1].items()}
        ]

    @staticmethod
    def lat_long_decoder(lat_long_code, lat_long_range):
        for i in lat_long_code:
            if i == '0':
                lat_long_range[1] = mean(lat_long_range)
            elif i == '1':
                lat_long_range[0] = mean(lat_long_range)
        return mean(lat_long_range)

    def geo_hash_to_decimal(self, geo_hash_string: str) -> [str, int]:
        decimal = 0
        for i in range(0, len(geo_hash_string)):
            decimal += (32 ** i) * self.geo_hash_dict[0][geo_hash_string[-i - 1]]
        return [geo_hash_string, decimal]

    def geo_hash_to_lat_log(self, geo_hash_string: str) -> [float, float]:
        lat_long_string = ""
        lat_range = [-90, 90]
        long_range = [-180, 180]
        for i in geo_hash_string:
            lat_long_string += self.geo_hash_dict[1][str(self.geo_hash_dict[0][i])]
        long_code = lat_long_string[0::2]
        lat_code = lat_long_string[1::2]
        return [self.lat_long_decoder(lat_code, lat_range), self.lat_long_decoder(long_code, long_range)]

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

    def lat_long_to_geo_hash(self, lat, long, precision: int = 40) -> str:
        lat_range = [-90, 90]
        long_range = [-180, 180]
        lat_code = self.hash_encoder(lat, lat_range, precision)
        long_code = self.hash_encoder(long, long_range, precision)
        # noinspection PyTypeChecker
        binaries = wrap(''.join([val for pair in zip(long_code, lat_code) for val in pair]), 5)
        geo_hash_out = ''
        for binary in binaries:
            geo_hash_out = geo_hash_out + self.geo_hash_dict_reverse[0][self.geo_hash_dict_reverse[1][binary]]
        return geo_hash_out

    def decimal_to_geo_hash(self):
        pass


if __name__ == '__main__':
    geo_hash = GeoHash()
    print(geo_hash.geo_hash_to_lat_log('ezs42s000esks2q2'))
    print(geo_hash.lat_long_to_geo_hash(42.605, -5.603))

