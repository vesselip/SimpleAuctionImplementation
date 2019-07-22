import unittest
from auction import Auction
from auction_engine import AuctionEngine
import io
from contextlib import redirect_stdout


class TestWinningBidsHandling(unittest.TestCase):

    def setUp(self):
        self.auction  = Auction(10, 7, 'car_1', 502.30, 20)
        self.auction.bid_list = [{'timestamp': 12, 'user_id': 8, 'item': 'car_1', 'bid_amount': 300.50},
                                  {'timestamp': 13, 'user_id': 5, 'item': 'car_1', 'bid_amount': 425.02},
                                  {'timestamp': 17, 'user_id': 8, 'item': 'car_1', 'bid_amount': 634.87}]

        self.auction.bid_list_duplicate = self.auction.bid_list.append({'timestamp': 18, 'user_id': 7, 'item': 'car_1',
                                                                     'bid_amount': 634.87})

        self.bid_summary = [(634.87,[{'timestamp': 17, 'user_id': 8, 'item': 'car_1', 'bid_amount': 634.87}]),
                            (425.02, [{'timestamp': 13, 'user_id': 5, 'item': 'car_1', 'bid_amount': 425.02}]),
                            (300.50,[{'timestamp': 12, 'user_id': 8, 'item': 'car_1', 'bid_amount': 300.50}])]

        self.bid_summary_duplicate = [(634.87,[{'timestamp': 18, 'user_id': 8, 'item': 'car_1', 'bid_amount': 634.87},
                                               {'timestamp': 17, 'user_id': 7, 'item': 'car_1','bid_amount': 634.87}]),
                                      (425.02, [{'timestamp': 13, 'user_id': 5, 'item': 'car_1', 'bid_amount': 425.02}]),
                                      (300.50,[{'timestamp': 12, 'user_id': 8, 'item': 'car_1', 'bid_amount': 300.50}])]

        self.auction_engine = AuctionEngine()
        self.auction_engine.add_auction(self.auction)

    def test_auction_simple_bid(self):

        highest_bid, lowest_bid, highest_bidder_id, price_paid= self.auction_engine.find_highest_bidder_and_price_paid(self.bid_summary, self.auction)
        self.assertEqual(highest_bid, 634.87)
        self.assertEqual(lowest_bid, 300.50)
        self.assertEqual(highest_bidder_id, 8)
        self.assertEqual(price_paid, 425.02)

    def test_auction_bid_duplicate(self):

        highest_bid, lowest_bid, highest_bidder_id, price_paid = self.auction_engine.find_highest_bidder_and_price_paid(self.bid_summary_duplicate, self.auction)
        self.assertEqual(highest_bid, 634.87)
        self.assertEqual(lowest_bid, 300.50)
        self.assertEqual(highest_bidder_id, 7)
        self.assertEqual(price_paid, 425.02)

    def test_bid_for_non_existing_item(self):
        bid = {}
        bid['timestamp'] = '20'
        bid['user_id'] = '6'
        bid['item'] = 'bed_1'
        bid['bid_amount'] = '65.3'

        self.auction_engine.place_bid(bid)
        self.assertRaises(RuntimeError)

    def test_bid_after_auction_ended(self):
        bid = {}
        bid['timestamp'] = '22'
        bid['user_id'] = '6'
        bid['item'] = 'car_1'
        bid['bid_amount'] = '65.3'

        expected = 'Auction is closed or bid arrived after auction ended for item car_1 time: 22'

        with io.StringIO() as buf, redirect_stdout(buf):
            self.auction_engine.place_bid(bid)
            output = buf.getvalue()
            self.assertEqual(expected, output.strip('\n'))

    def test_abid_user_lower_than_previous_bid(self):
        bid = {}
        bid['timestamp'] = '19'
        bid['user_id'] = '5'
        bid['item'] = 'car_1'
        bid['bid_amount'] = '100.33'

        self.auction_engine.place_bid(bid)
        result = [x for x in self.auction.bid_list if x['user_id'] == 5 and float(x['bid_amount']) == 100.33]

        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
