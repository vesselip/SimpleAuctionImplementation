import unittest
from auction_orchestrator import AuctionDataParser


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.parser = AuctionDataParser([], None)

        # pass string instead of int
        self.sell = ['10', 'M', 'SELL', 'toaster_1', '10.00', '20']
        # pass invalid bid
        self.bid = ['12', '8', 'BID', 'toaster_1', '-7.50']

    def test_SELL(self):
        self.parser.validate(self.sell, 'SELL')
        self.assertRaisesRegex(ValueError, "invalid literal for.*XYZ'$", int, 'XYZ')

    def test_BID(self):
        self.parser.validate(self.bid, 'BID')
        self.assertRaises(RuntimeError)

if __name__ == '__main__':
    unittest.main()