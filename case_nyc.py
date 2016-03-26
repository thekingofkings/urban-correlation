"""
Hongjian
3/26/2016


all tweets related case in NYC

case 1:
    NYCC (new york comic con) in Jacob center
"""




from matplotlib.pyplot import *
from TweetGroup import TweetGroup
from pre_processing_function import location




def case(twtG, tags=[]):
    """Tweet tags in one tweetGroup
    
    Known pair: 
    
    1) nycc@jacob center
    twtG = jacobTwt
    tags = ["#nycc", "#nycomiccon", "#nycc2012"]
    
    2) cmj@MSG
    twtG = msgTwt
    tags = ["#cmj"]
    
    return value: time series of the tweets (by hour)
    """
    ht, sortht = twtG.top_k_hashtag(20)
    caseTwt = twtG.filter_tweets_by_hashtag(tags=tags)
    ts = caseTwt.generate_timeSeries()
    
    return ts
    
    
    
def plot_nycc_2012_jacob_case(jacobTwt):
    
    # get the time series of tweets with "nycc" related tag
    ts = case(jacobTwt, ["#nycc", "#nycomiccon", "#nycc2012"])

    # plot
    figure(figsize=(15,5))
    plot(ts[120:384], 'b-', linewidth=3)
    import pickle
    traff = pickle.load(open("taxi_tsjacob.pickle", "rU"))
    tpick = traff["taxi_pick_"]
    tdrop = traff["taxi_drop_"]
    plot(tpick[120:384], "r-", linewidth=3)
    plot(tdrop[120:384], "g-", linewidth=3)
    axvline(252 - 120, color='black', ls=':', lw=3)
    axvline(276 - 120, color='black', ls=':', lw=3)
    axvline(300 - 120, color='black', ls=':', lw=3)
    axvline(324 - 120, color='black', ls=':', lw=3)
    #title("Jacob center - pickup - dropoff - #nycc")
    xticks( range(12, 265, 24), ["10/{0:02d}".format(i) for i in range(6, 20, 1)] )
    xlim(0, 264)
    ylabel("Count of traffic and tweets", fontsize=16)
    xlabel("Dates in 2012", fontsize=16)
    legend(("#nycc", "Pickup", "Dropoff"), loc=2)
    savefig("jacob-small-box.png", format="png")
    return ts
    
    
    
    
    


if __name__ == '__main__':
    

    fname = "nyc-tweets-12"
    all_tweets = TweetGroup(fname="{0}.csv".format(fname))        
    jacobTwt = all_tweets.filter_tweets_by_bbox(location['jacob'])
    tsTwt = all_tweets.filter_tweets_by_bbox(location['timesquare'])
    msgTwt = all_tweets.filter_tweets_by_bbox(location['msg'])
        
        
    plot_nycc_2012_jacob_case(jacobTwt)
    
    
    # nyccTwt = r[1]
    # t = jacobTwt.filter_tweets_by_timeWindow("20121019", "20121019235959")
    # t.saveToFile("2012-10-19")
    # print t.top_k_hashtag(20)[1]
        
        
    
    
#    r2 = case(msgTwt, ["#cmj"])
    
#    r3 = case(tsTwt, ["#pivotcon"])
    
#    case(msgTwt, ["#cmj"])
#    case(jacobTwt, ["#cmj"])
    

    
    
    
    
#    ht, ht_list = all_tweets.top_k_hashtag(1000)
        
#    with open("{0}-poptag.csv".format(fname), "w") as fout:
#        for twt in all_tweets.tweets:
#            twt.set_popular_tag(ht)
#            fout.write(str(twt) + "\n")
            
            
    
