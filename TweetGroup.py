"""
Hongjian
3/26/2016


Factor the TweetGroup class into one file
"""


from Tweet import Tweet



class TweetGroup:
    
    
    
    def __init__(self, tweets=[], fname=''):
        """Build a tweet group from a list of tweets"""
        self.tweets = tweets
        if fname != '':
            # read all tweets from given file
            with open(fname, "r") as fin:
                for line in fin:
                    ls = line.split(",", 5)
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
        
        
        
    def __len__(self):
        """override length function"""
        return len(self.tweets)



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
                    break
            
        return TweetGroup(res)
        
        
    
    def generate_timeSeries(self, tstype="tweets"):
        """ generate a count time series 
        
        Input:
        tstype -- the type of time series, takes value
            "tweets" or "users"
        """
        if tstype == "tweets":
            TS = {}
            for twt in self.tweets:
                k = twt.timestamp[:10]
                if k in TS:
                    TS[k] += 1
                else:
                    TS[k] = 1
                    
            n = []
            for month in range(10,12):
                for day in range(1, 32):
                    for hour in range(24):
                        k = '2012{0:02d}{1:02d}{2:02d}'.format(month, day, hour)
                        if k in TS:
                            n.append(TS[k])
                        else:
                            n.append(0)
            return n
        elif tstype == "users":
            TS = {}
            for twt in self.tweets:
                k = twt.timestamp[:10]
                if k in TS:
                    if twt.uid not in TS[k]:
                        TS[k].add(twt.uid)
                else:
                    TS[k] = set()
                    TS[k].add(twt.uid)
            
            n = []
            for month in range(10,12):
                for day in range(1, 32):
                    for hour in range(24):
                        k = '2012{0:02d}{1:02d}{2:02d}'.format(month, day, hour)
                        if k in TS:
                            n.append(len(TS[k]))
                        else:
                            n.append(0)
            return n
            
            
            
        
    
    def count_hashtag(self, tag, byUser=False):
        """ count how many tweets contain the given hashtag """
        if not byUser:    
            cnt = 0
            for twt in self.tweets:
                if tag in twt.hashtag:
                    cnt += 1
            return cnt
        else:
            users = set()
            for twt in self.tweets:
                if twt.uid not in users:
                    users.add(twt.uid)
            return len(users)
        
        
        
    def count_unique_user(self):
        """ count number of unique users """
        uc = set()
        for twt in self.tweets:
            if twt.uid not in uc:
                uc.add(twt.uid)
        
        return len(uc)

    
    
    def filter_tweets_by_timeWindow(self, start_prefix, end_prefix):
        """filter tweets by time window
        
        the timestamp is a string of length 17.
        The start_prefix and end_prefix give the timestamp range"""
        start_ = start_prefix + "0" * (17 - len(start_prefix))
        end_ = end_prefix + "0" * (17 - len(end_prefix))
        
        res = []
        for twt in self.tweets:
            if twt.timestamp >= start_ and twt.timestamp <= end_:
                res.append(twt)
                
        return TweetGroup(res)
        
        
    def saveToFile(self, fname):
        with open(fname, 'w') as fout:
            for t in self.tweets:
                fout.write(str(t) + "\n")
                
                
    def split_tweets_byDay(self):
        """ split tweets by day """
        splits = {}
        for twt in self.tweets:
            k = twt.timestamp[:8]
            if k in splits:
                splits[k].append(twt)
            else:
                splits[k] = [twt]
        
        self.splits = {}
        for k in splits:
            self.splits[k] = TweetGroup(splits[k])
        return self.splits
                
        