# import logging
import unittest

from aurum.package_tracker import installed_packages_hash


# logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class PackageTrackerTestCase(unittest.TestCase):

    def test_installed_packages_hashing(self):
        # Testing the exact hash would couple this test to the projects dependencies.
        package_hash = installed_packages_hash()
        self.assertIsInstance(package_hash, str)


if __name__ == '__main__':
    unittest.main()
