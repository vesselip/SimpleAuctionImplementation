from operator import itemgetter
from itertools import groupby


class AuctionEngine():
    '''
    Holds a record of all auctions with methods that operate on them
    '''

    def __init__(self):
        self.auctions = {}

    def add_auction(self, auction):
        self.auctions[auction.item] = auction

    def check_auctions(self, timestamp):
        '''
        Goes through all auctions if the current time is after auction's close time closes the auction
        :param timestamp:
        :return:
        '''
        for auction in self.auctions.values():
            if auction.close_time <= timestamp:
                auction.open = False
                self.produce_auction_summary(auction)

    def produce_auction_summary(self, auction):
        '''
        For given auction we sort all bids from highest to lowest
        :param auction:
        :return:
        '''
        auction.bid_list.sort(key=itemgetter('bid_amount'), reverse=True)

        bid_summary = []
        for bid_amount, items in groupby(auction.bid_list, key=itemgetter('bid_amount')):
            bid_summary_items = []
            for i in items:
                bid_summary_items.append(i)

            bid_summary.append((bid_amount, bid_summary_items))

        total_bid_count = sum([len(x[1]) for x in bid_summary])

        highest_bidder_id = None
        highest_bid = 0.0
        lowest_bid = 0.0
        price_paid = 0.0

        if len(bid_summary) >= 1:
            highest_bid, lowest_bid, highest_bidder_id, price_paid = self.find_highest_bidder_and_price_paid(bid_summary, auction)

        auction.summary = "{}|{}|{}|{}|{}|{}|{}|{}".format(auction.close_time, auction.item, highest_bidder_id,
                                                        auction.status, price_paid, total_bid_count, highest_bid,
                                                        lowest_bid)

    def place_bid(self, bid):
        auction = self.auctions.get(bid['item'])

        try:
            if not auction:
                raise RuntimeError('No auction exists for: {}'.format(bid['item']))

            if auction and auction.open and auction.close_time >= int(bid['timestamp']) and auction.timestamp < int(bid['timestamp']):
                # here check if user already placed a bid and if so the current bid is higher than previous one
                if len([x for x in auction.bid_list if x['user_id'] == int(bid['user_id']) and float(x['bid_amount']) >= float(bid['bid_amount'])]) == 0:
                    auction.bid_list.append(bid)
            else:
                print('Auction is closed or bid arrived after auction ended for item {} time: {}'.format(bid['item'], bid['timestamp']))
        except Exception as e:
            print(e)

    def find_highest_bidder_and_price_paid(self, bid_summary, auction):
        '''
        Here we resolve scenario when 2 or more bids are placed with the same winning amount then pick the bid with
        earliest timestamp. We assume that the two bids would have been placed at different times
        :param bid_summary: bid summary ordered list of tuples bid amount and 1 or more dict(s) with bid detail's
        :param auction: the auction object for this auction
        :return: tuple highest_bid, lowest_bid, highest_bidder_id
        '''
        highest_bidder_id = None
        highest_bid = round(bid_summary[0][0], 2)
        lowest_bid = round(bid_summary[-1][0], 2)
        price_paid = 0.0

        if bid_summary[0][0] >= auction.reserve_price:
            auction.status = 'SOLD'
            # check we only have one valid bid then return the reserved price
            if len(bid_summary) == 1:
                return bid_summary[0][1][0]['bid_amount'], bid_summary[0][1][0]['bid_amount'], bid_summary[0][1][0]['user_id'], auction.reserve_price
            if len(bid_summary[0][1]) > 1:
                bid_summary[0][1].sort(key=itemgetter('timestamp'))
                result_list = []
                for timestamp, items in groupby(bid_summary[0][1], key=itemgetter('timestamp')):
                    for i in items:
                        result_list.append(i)
                highest_bidder_id = result_list[0]['user_id']
            else:
                highest_bidder_id = bid_summary[0][1][0]['user_id']

            if len(bid_summary) == 1:
                price_paid = bid_summary[0][0] if auction.status == 'SOLD' else 0.0
            else:
                price_paid = bid_summary[1][0] if auction.status == 'SOLD' else 0.0

        return highest_bid, lowest_bid, highest_bidder_id, price_paid

    def list_auctions_outcomes(self):
        '''
        Iterates through all auctions prints the summary
        :return:
        '''

        for auction in self.auctions.values():
            auction.get_summary()