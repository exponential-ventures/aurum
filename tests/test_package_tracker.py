# import logging
import unittest

from aurum.package_tracker import installed_packages_hash


# logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class PackageTrackerTestCase(unittest.TestCase):

    def test_installed_packages_hashing(self):
        # We can't really test more than this, testing the exact hash would couple this test to the
        # projects dependencies so for now this just tests if the function can be called without an error and can return
        # a str.
        package_hash = installed_packages_hash()
        self.assertIsInstance(package_hash, str)


if __name__ == '__main__':
    unittest.main()
