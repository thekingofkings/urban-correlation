"""
Hongjian
3/26/2016


all tweets related case in NYC

case 1:
    NYCC (new york comic con) in Jacob center
    
    1) nycc@jacob center
    twtG = jacobTwt
    tags = ["#nycc", "#nycomiccon", "#nycc2012"]

    2) cmj@MSG
    twtG = msgTwt
    tags = ["#cmj"]
"""




from matplotlib.pyplot import *
from TweetGroup import TweetGroup
from pre_processing_function import location
import pickle
from math import log




def hashtag_measure( subTwtGrp, allTwtGrp, hashtags):
    """Measure for hashtag
    
    Input:
    1) subTwtGrp - the tweets of focal region
    2) allTwtGrp - all tweets in NYC
    3) hashtags - a list of hashtags that we use for calculating measure
    
    Output:
    some measure
    """
    idf = calc_idf(allTwtGrp, hashtags)
    print "============ another day =================="
    ttn = len(subTwtGrp.tweets)
    ratio = 0.0
    for tag in hashtags:
        cnt_sub = subTwtGrp.count_hashtag(tag)
#        cnt_all = allTwtGrp.count_hashtag(tag)
#        ratio += cnt_sub / float(cnt_all)

#        ratio += cnt_sub
        
        ratio += cnt_sub * idf[tag] / float(ttn)
        print tag, cnt_sub / float(ttn), idf[tag], cnt_sub * idf[tag] / float(ttn)
        
    return ratio #* len(subTwtGrp.tweets)
#    return len(subTwtGrp.tweets)
        




def calc_idf(twtGrp, hashtags):
    df_cnt = {}
    for tag in hashtags:
        df_cnt[tag] = set()
        for twt in twtGrp.tweets:
            gridk = twt.location_key()
            if tag in twt.hashtag and gridk not in df_cnt[tag]:
                df_cnt[tag].add(gridk)
                
    idf = {}
    for tag in hashtags:
        tmp = log(10000.0 / len(df_cnt[tag]))
        idf[tag] = tmp if tmp > 5 else 0
    
    return idf



    
def plot_nycc_2012_jacob_case(jacobTwt):
    
    # get the time series of tweets with "nycc" related tag
    tagTwt = jacobTwt.filter_tweets_by_hashtag(["#nycc", "#nycomiccon", "#nycc2012"])
    ts = tagTwt.generate_timeSeries()

    # plot
    figure(figsize=(15,5))
    plot(ts[120:384], 'b-', linewidth=3)
    
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
    
    
    

def merge_taxi_count_into_day():
    traff = pickle.load(open("taxi_tsjacob.pickle", "rU"))
    
    tpick = traff["taxi_pick_"]
    tdrop = traff["taxi_drop_"]
    
    dpick = []
    ddrop = []
    
    for i in range(31):
        dpick.append(sum(tpick[i*24:i*24+24]))
        ddrop.append(sum(tdrop[i*24:i*24+24]))
        
    return dpick, ddrop


if __name__ == '__main__':
    

    fname = "nyc-tweets-12"
    all_tweets = TweetGroup(fname="{0}.csv".format(fname))
    
    all_dmap = all_tweets.split_tweets_byDay()
    
    
    
    jacobTwt = all_tweets.filter_tweets_by_bbox(location['jacob'])
    tsTwt = all_tweets.filter_tweets_by_bbox(location['timesquare'])
    msgTwt = all_tweets.filter_tweets_by_bbox(location['msg'])
        
        
#    plot_nycc_2012_jacob_case(jacobTwt)
        
    dmap = jacobTwt.split_tweets_byDay()
    sortedKey = dmap.keys()
    sortedKey.sort()
    
    
    ratio = []
    for k in sortedKey:
        hashtags = dmap[k].top_k_hashtag(20)[0].keys()
        ratio.append(hashtag_measure(dmap[k], all_dmap[k], hashtags))
        
        
    traff = merge_taxi_count_into_day()
    
    f,ax1 = subplots()
    ax1.plot(ratio)
    ax1.set_ylabel("Hashtag measure")
    legend(("hashtag",), loc=2)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    ax2 = ax1.twinx()
    ax2.plot(traff[0], "r--")
    ax2.plot(traff[1], "g:")
    ax1.set_ylabel("Traffic count")
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    legend(("Pickup", "Dropoff"), loc=1)
    
    savefig("tweets-tag-tfidf-traffic.pdf")
    
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
            
            
    
