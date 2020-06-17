import unittest
from geohash import Geohash


class GeohashUnittest(unittest.TestCase):

    def test_something(self):
        print()
        for hash_kind in [32, 64, 256, 4096]:
            print(f"Testing: {hash_kind}ghs")
            geo_hash = Geohash(hash_type=hash_kind)
            lat_long_pair = [-5.6034, 42.6057]
            calculated_hash = geo_hash.lat_long_to_geo_hash(lat_long_pair[0], lat_long_pair[1])
            calculated_nums = [round(x, 4) for x in geo_hash.geo_hash_to_lat_long(calculated_hash)]

            self.assertEqual(lat_long_pair, calculated_nums)

            if hash_kind in [256, 4096]:
                print(f"\tTesting quartets for: {hash_kind}ghs")
                quartet = [-5.6034, 42.6057, 4.8153, -0.6849]
                calculated_hash = geo_hash.lat_long_theta_phi_to_geo_hash(*quartet)
                calculated_nums = [round(x, 4) for x in geo_hash.geo_hash_to_lat_long_theta_phi(calculated_hash)]
                self.assertEqual(quartet, calculated_nums)
                if hash_kind == 4096:
                    sextet = [-5.603, 42.605, 4.815615568277845, -0.6845378023414236, 1]

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
