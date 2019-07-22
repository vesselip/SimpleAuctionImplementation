import unittest
from auction_orchestrator import AuctionDataParser
from auction_engine import AuctionEngine
import os
import io
from contextlib import redirect_stdout


class TestIntegratedAuctionSystem(unittest.TestCase):

    def setUp(self):
        self.file_location = 'tests/data'
        self.file_name = 'input.txt'

        file_path = os.path.join(self.file_location, self.file_name)

        with open(file_path, 'r') as f:
            data = f.read()

        self.auction_engine = AuctionEngine()
        self.parser = AuctionDataParser(data, self.auction_engine)

    def test_auction_results(self):
        self.parser.parse_input()

        with io.StringIO() as buf, redirect_stdout(buf):
            self.parser.get_auction_engine().list_auctions_outcomes()
            output = buf.getvalue()
            lines = [x for x in output.splitlines()]
            self.assertEqual(lines[0], '20|toaster_1|8|SOLD|12.5|3|20.0|7.5')
            self.assertEqual(lines[1], '20|tv_1|None|UNSOLD|0.0|2|200.0|150.0')


if __name__ == '__main__':
    unittest.main()