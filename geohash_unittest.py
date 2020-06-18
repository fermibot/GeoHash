import unittest
from geohash import Geohash
from random import random


class GeohashUnittest(unittest.TestCase):

    def pair_cases(self, hash_instance, pair):
        calculated_hash = hash_instance.nums_to_geohash(pair)
        calculated_nums = [round(x, 7) for x in hash_instance.hash_to_nums(calculated_hash, split_type=2)]
        self.assertEqual(pair, calculated_nums)

    def test_all_geohash_use_cases(self):
        print()
        for hash_kind in [32, 64, 256, 4096]:
            print(f"Testing pairs for {hash_kind}ghs")
            geohash_inst = Geohash(hash_type=hash_kind)

            lat_long_pair = [-5.6034751, 42.6057093]
            calculated_hash = geohash_inst.nums_to_geohash(lat_long_pair)
            calculated_nums = [round(x, 7) for x in geohash_inst.hash_to_nums(calculated_hash, split_type=2)]
            self.assertEqual(lat_long_pair, calculated_nums)

            for pairs in range(10):
                pair = [round(x, 7) for x in [180 * 2 * (random() - 0.5), 90 * 2 * (random() - 0.5)]]
                self.pair_cases(geohash_inst, pair)

            if hash_kind in [256, 4096]:
                print(f"\tTesting quartets for {hash_kind}ghs")
                quartet = [-5.6034, 42.6057, 4.8153, -0.6849]
                calculated_hash = geohash_inst.nums_to_geohash(quartet)
                calculated_nums = [round(x, 4) for x in geohash_inst.hash_to_nums(calculated_hash, split_type=4)]
                self.assertEqual(quartet, calculated_nums)
                if hash_kind == 4096:
                    print(f"\t\tTesting sextets for {hash_kind}ghs")
                    sextet = [-5.6034, 42.6057, 4.8153, -0.6849, 5.9462, 54.6548]
                    calculated_hash = geohash_inst.nums_to_geohash(sextet)
                    calculated_nums = [round(x, 4) for x in
                                       geohash_inst.hash_to_nums(calculated_hash, split_type=6)]
                    self.assertEqual(sextet, calculated_nums)

    def test(self):
        assert (True, True)


if __name__ == '__main__':
    unittest.main()
