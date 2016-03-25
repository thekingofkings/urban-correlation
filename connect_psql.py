import psycopg2
import re
from pre_processing_function import *
from matplotlib import get_backend
print get_backend()


from matplotlib.pyplot import plot, figure, title, legend, show, savefig
import numpy as np


def retrieve_data_from_db_server():
    conn = psycopg2.connect(host="lrs-jli02.ist.psu.edu", database="postgres", user="hxw186", password="hxw186")
    
    cur = conn.cursor()
    
    
    # the lon, lat is in NYC, the text contains hashtag
    cur.execute("""SELECT tweetid, timestamp, lon, lat, text from usatweets where lat <= 40.87705 
                AND lat >= 40.698991 AND lon <= -73.917046 AND lon >= -74.020042 AND 
                text ~* '.*#\w+.*'; """)
    
    cnt = 0
    with open("nyc-tweets-12.csv", "w") as fout12, open("nyc-tweets-13.csv", "w") as fout13:            
        while True:
            res = cur.fetchmany(100)
            if not res:
                print "finished. ready to exit!"
                break
            
            for row in res:
                cnt += 1
                if cnt % 1000 == 0:
                    print cnt
                t = str(row[1])
                if t[0:6] == "201210":
                    fout12.write("{0},{1},{2},{3},{4}\n".format(*row))
                elif t[0:6] == "201306":
                    fout13.write("{0},{1},{2},{3},{4}\n".format(*row))
        
        
        
        
class Tweet:
    
    hist_hashtag = {}
    
    
    def __init__(self, tid, timestamp, lon, lat, text):
        self.tid = int(tid)
        self.timestamp = timestamp
        self.timestamp += "0" * (17 - len(self.timestamp))    # fix all timestamp length as 17
        self.lon = float(lon)
        self.lat = float(lat)
        tags = re.findall("#\w+", text.strip())
        self.hashtag = [s.lower() for s in tags]
        
    
    def __str__(self):
        """override __str__ for output"""
        return "{0},{1},{2},{3},{4}".format(self.tid, self.timestamp, self.lon, self.lat, self.poptag)
        
        
        
    def set_popular_tag(self, poptags):
        """Find the most popular tag of current tweets"""
        self.poptag = 1000000
        for s in self.hashtag:
            if s in poptags and poptags[s] < self.poptag:
                self.poptag = poptags[s]
        
        if self.poptag == 1000000:
            self.poptag = -1
            
            
            
    def get_timestamp(self):
        return date2linux_timestamp( self.timestamp[:14], "%Y%m%d%H%M%S" )
            
            
        
    def toList(self):
        return [date2linux_timestamp( self.timestamp[:14], "%Y%m%d%H%M%S" ), self.lon, self.lat, self.poptag ]
        
        
    def inBbox(self, bbox):
        if float(self.lon) <= bbox[1][0] and float(self.lon) >= bbox[0][0] \
                and float(self.lat) <= bbox[1][1] and float(self.lat) >= bbox[0][0]:
            return True
        else:
            return False
    
    
    
class TweetGroup:
    
    
    
    def __init__(self, tweets=[], fname=''):
        """Build a tweet group from a list of tweets"""
        self.tweets = tweets
        if fname != '':
            # read all tweets from given file
            with open(fname, "r") as fin:
                for line in fin:
                    ls = line.split(",", 4)
                    twt = Tweet(*ls)
                    self.tweets.append(twt)
        
        # generate hash_tag_map
        hashtag_map = {}
        for t in self.tweets:
            for s in t.hashtag:
                if s in hashtag_map:
                    hashtag_map[s] += 1
                else:
                    hashtag_map[s] = 1
        self.hist_hashtag = hashtag_map
        
        

    def top_k_hashtag(self, k):
        sorted_tuple = sorted(self.hist_hashtag.items(), key=lambda x : x[1], reverse=True)
        poptags = {}
        for i in range(k):
           poptags[sorted_tuple[i][0]] = i
        return poptags, sorted_tuple[:k]


    def filter_tweets_by_bbox(self, bbox):
        """filter tweets by bbox
        
        bbox = ( bottom-left, up-right )
        """
        res = []
        for t in self.tweets:
            if (t.inBbox(bbox)):
                res.append(t)
        return TweetGroup(res)

    
    
    def filter_tweets_by_hashtag(self, tags=[]):
        """filter tweets by tags
        
        tags = [ a list of tags refering the same thing ]
        """
        res = []
        
        for t in self.tweets:
            for tag in tags:
                if tag in t.hashtag:
                    res.append(t)
            
        return TweetGroup(res)
        
        
    
    def generate_timeSeries(self):
        """ generate a tweet count time series """
        TS = []
        for twt in self.tweets:
            TS.append(twt.get_timestamp())
        
        n, bins = np.histogram(TS, bins=24*31)
        return n




def case(twtG, tags=[]):
    """Tweet tags in one tweetGroup
    
    Known pair: 
    
    1) nycc@jacob center
    twtG = jacobTwt
    tags = ["#nycc", "#nycomiccon", "#nycc2012"]
    
    2) cmj@MSG
    twtG = msgTwt
    tags = ["#cmj"]
    """
    ht, sortht = twtG.top_k_hashtag(20)
    caseTwt = twtG.filter_tweets_by_hashtag(tags=tags)
    ts = caseTwt.generate_timeSeries()
    figure()
    plot(ts)
    return ts
    

    
if __name__ == '__main__':
    
    task = "1query_data"
    
    if task == "query_data":
        retrieve_data_from_db_server()
    else:
        fname = "nyc-tweets-12"
        all_tweets = TweetGroup(fname="{0}.csv".format(fname))
        jacobTwt = all_tweets.filter_tweets_by_bbox(location['jacob'])
        tsTwt = all_tweets.filter_tweets_by_bbox(location['timesquare'])
        msgTwt = all_tweets.filter_tweets_by_bbox(location['msg'])
        
        
        
        r = case(jacobTwt, ["#nycc", "#nycomiccon", "#nycc2012"])
        
        import pickle
        traff = pickle.load(open("taxi_tsjacob.pickle", "rU"))
        tpick = traff["taxi_pick_"]
        tdrop = traff["taxi_drop_"]
        plot(tpick, "r-")
        plot(tdrop, "g:")
        title("Jacob center - pickup - dropoff - #nycc")
        legend(("#nycc", "Pickup", "Dropoff"))
        show()
        savefig("jacob-small-box.pdf", format="pdf")

    
    
#    r2 = case(msgTwt, ["#cmj"])
    
#    r3 = case(tsTwt, ["#pivotcon"])
    
#    case(msgTwt, ["#cmj"])
#    case(jacobTwt, ["#cmj"])
    

    
    
    
    
#    ht, ht_list = all_tweets.top_k_hashtag(1000)
        
#    with open("{0}-poptag.csv".format(fname), "w") as fout:
#        for twt in all_tweets.tweets:
#            twt.set_popular_tag(ht)
#            fout.write(str(twt) + "\n")
            
            
    