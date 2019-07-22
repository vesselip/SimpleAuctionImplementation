
class Auction():
    '''
    Class representing an auction
    '''
    def __init__(self, timestamp, user_id, item, reserve_price, close_time):
        self.timestamp = timestamp
        self.user_id = user_id
        self.item = item
        self.reserve_price = reserve_price
        self.close_time = close_time
        self.bid_list = []
        self.open = True
        self.summary = None
        self.status = 'UNSOLD'

    def get_summary(self):
        '''
        Prints summary of the auction like so
        close_time|item|user_id|status|price_paid|total_bid_count|highest_bid|lowest_bid
        :return:
        '''
        print(self.summary)