import argparse
import os
from auction import Auction
from auction_engine import AuctionEngine

class AuctionDataParser:
    '''
    Validates the input to the AuctionEngine then calls the appropriate for the given action i.e SELL/BID/HEARTBEAT
    '''

    def __init__(self, data, auction_engine):
        self.data = data
        self.auction_engine = auction_engine
        self.parse_input()

    def parse_input(self):
        if isinstance(self.data, str):
            for row in self.data.splitlines():
                tokens_list = row.split('|')
                if 'SELL' in tokens_list and self.validate(tokens_list, 'SELL'):
                    # Auction(timestamp, user_id, item, reserve_price, close_time)
                    auction = Auction(int(tokens_list[0]), int(tokens_list[1]),
                                      str(tokens_list[3]), float(tokens_list[4]),
                                      int(tokens_list[5]))
                    self.auction_engine.add_auction(auction)
                elif 'BID' in tokens_list and self.validate(tokens_list, 'BID'):
                    bid = {}
                    bid['timestamp'] = int(tokens_list[0])
                    bid['user_id'] = int(tokens_list[1])
                    bid['item'] = str(tokens_list[3])
                    bid['bid_amount'] = float(tokens_list[4])

                    self.auction_engine.place_bid(bid)
                elif len(tokens_list) == 1 and self.validate(tokens_list, 'HEARTBEAT'):
                    self.auction_engine.check_auctions(int(tokens_list[0]))
                else:
                    raise RuntimeError('Unsupported action for: {}'.format(row))

    def validate(self, tokens_list, action_type):

        if action_type == 'SELL':
            if len(tokens_list) == 6:
                try:
                    if isinstance(int(tokens_list[0]), int) \
                            and isinstance(int(tokens_list[1]), int)\
                            and isinstance(tokens_list[2], str) and tokens_list[2] == 'SELL'\
                            and isinstance(tokens_list[3], str) \
                            and isinstance(float(tokens_list[4]), float)\
                            and isinstance(int(tokens_list[5]), int):
                        return True
                    else:
                        return False
                except ValueError as e:
                    print(e)
            else:
                raise RuntimeError('Expected {} tokens for SELL action got {}'.format(6, len(tokens_list)))
        elif action_type == 'BID':
            if len(tokens_list) == 5:
                try:
                    if isinstance(int(tokens_list[0]), int) \
                            and isinstance(int(tokens_list[1]), int)\
                            and isinstance(tokens_list[2], str) and tokens_list[2] == 'BID'\
                            and isinstance(tokens_list[3], str) \
                            and isinstance(float(tokens_list[4]), float):
                        if float(tokens_list[4]) <= 0.0:
                            raise RuntimeError('Bid must be non zero and positive number')
                        return True
                    else:
                        return False
                except ValueError as e:
                    print(e)
                except Exception as e:
                    print(e)
            else:
                raise RuntimeError('Expected {} tokens for BID action got {}'.format(5, len(tokens_list)))
        elif action_type == 'HEARTBEAT':
            if len(tokens_list) == 1:
                if isinstance(int(tokens_list[0]), int):
                    return True
                else:
                    return False
            else:
                raise RuntimeError('Expected {} tokens for HEARTBEAT action got {}'.format(1, len(tokens_list)))

    def get_auction_engine(self):
        return self.auction_engine


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Auction data parser')
    parser.add_argument("--file_location", action='store', dest="file_location", help="Sets location of the input file")
    parser.add_argument("--file_name", action='store', dest="file_name", help="Sets name of the input file")

    args = parser.parse_args()

    file_path = os.path.join(args.file_location, args.file_name)

    with open(file_path, 'r') as f:
        data = f.read()

    auction_engine = AuctionEngine()
    parser = AuctionDataParser(data, auction_engine)
    parser.parse_input()
    parser.get_auction_engine().list_auctions_outcomes()
