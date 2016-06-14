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



import matplotlib
matplotlib.use('agg')
from matplotlib.pyplot import *
from TweetGroup import TweetGroup
from pre_processing_function import location
import pickle
from math import log




def hashtag_measure( subTwtGrp, allTwtGrp, hashtags, measure="tweetCount"):
    """Measure for hashtag
    
    Input:
    1) subTwtGrp - the tweets of focal region
    2) allTwtGrp - all tweets in NYC
    3) hashtags - a list of hashtags that we use for calculating measure
    4) measure - could be the following
        a. tweetCount
        b. uniqueUserCount
        c. top#-tf
        d. top#-tfidf
        e. top#-tf-byuser
        f. top#-relaCnt
    
    Output:
    some measure
    """
    if measure == "uniqueUserCount":
        return subTwtGrp.count_unique_user()
    elif measure == "tweetCount":
        return len(subTwtGrp.tweets)
    elif measure == "top#-tf":
        ratio = 0.0
        for tag in hashtags:
            ratio += subTwtGrp.count_hashtag(tag)
        return ratio
    elif measure == "top#-tfidf":
        idf = calc_idf(allTwtGrp, hashtags)
        ratio = 0.0
        for tag in hashtags:
            cnt_sub = subTwtGrp.count_hashtag(tag)
            ratio += cnt_sub * idf[tag]
        return ratio
    elif measure == "top#-tf-byuser":
        ratio = 0.0
        for tag in hashtags:
            ratio += subTwtGrp.count_hashtag(tag, byUser=True)
        return ratio
    elif measure == "top#-relaCnt":
        ratio = 0.0
        for tag in hashtags:
            cnt_sub = subTwtGrp.count_hashtag(tag)
            cnt_all = allTwtGrp.count_hashtag(tag)
            ratio += cnt_sub / float(cnt_all)
        return ratio
      




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
    ts = tagTwt.generate_timeSeries(tstype="users")
    pickle.dump(ts, open("data/tweets_jacob_nycc.pickle", 'w'))

    traff = pickle.load(open("data/taxi_tsjacob.pickle", "rU"))
    tpick = traff["taxi_pick_"]
    tdrop = traff["taxi_drop_"]

    # plot
    figure(figsize=(15,5))
    ax1 = subplot()
    
        
        
    
    l2 = ax1.plot(tpick[120:384], "r-", linewidth=3)
    l3 = ax1.plot(tdrop[120:384], "b-", linewidth=3)
    axvline(252 - 120, color='black', ls=':', lw=3)
    axvline(276 - 120, color='black', ls=':', lw=3)
    axvline(300 - 120, color='black', ls=':', lw=3)
    axvline(324 - 120, color='black', ls=':', lw=3)
    ax1.set_ylabel("Count of traffic", fontsize=24)

    #title("Jacob center - pickup - dropoff - #nycc")
    xticks( range(12, 265, 24), ["10/{0:02d}".format(i) for i in range(6, 20, 1)], fontsize=20 )
    xlim(0, 264)
    legend(("Pickup", "Dropoff"), loc=2, fontsize=24)
    
    
    ax2 = ax1.twinx()
    l1 = ax2.plot(ts[120:384], ls="-", color="green", linewidth=4)
    ax2.set_ylim((0,50))
    
    
    for tl in ax2.get_yticklabels():
        tl.set_color('g')
        
        
    ax2.set_ylabel("Count of tweets", fontsize=24)
    xlabel("Dates in 2012", fontsize=24)
    legend(("#nycc",), loc=1, fontsize=24)
    savefig("fig/jacob-small-box.pdf")
    return ts
    
    
    

def merge_taxi_count_into_day():
    traff = pickle.load(open("data/taxi_tsjacob.pickle", "rU"))
    
    tpick = traff["taxi_pick_"]
    tdrop = traff["taxi_drop_"]
    
    dpick = []
    ddrop = []
    
    for i in range(31):
        dpick.append(sum(tpick[i*24:i*24+24]))
        ddrop.append(sum(tdrop[i*24:i*24+24]))
        
    return dpick, ddrop



def find_tweets_measure_toMatch_traffic():

    fname = "nyc-tweets-12"
    all_tweets = TweetGroup(fname="data/{0}.csv".format(fname))
    
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
    ax2.set_ylabel("Traffic count")
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    legend(("Pickup", "Dropoff"), loc=1)
    
    savefig("fig/tweets-user-count-traffic.pdf")
    
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
            
            
    

def get_userCnt_TS():
    
    fname = "nyc-tweets-12"
    tmp_tweets = TweetGroup(fname="data/{0}.csv".format(fname))
    tmp_len = len(tmp_tweets)
    all_tweets = TweetGroup(tweets=tmp_tweets.tweets, fname="data/nyc-tweets-1211.csv")
    assert len(all_tweets) > tmp_len
    
    
    jacobTwt = all_tweets.filter_tweets_by_bbox(location['jacob'])
    tsTwt = all_tweets.filter_tweets_by_bbox(location['timesquare'])
    msgTwt = all_tweets.filter_tweets_by_bbox(location['msg'])
    E58Twt = all_tweets.filter_tweets_by_bbox(location['58E'])
    
    
    t1 = jacobTwt.generate_timeSeries(tstype="users")
    t2 = tsTwt.generate_timeSeries("users")
    t3 = msgTwt.generate_timeSeries("users")
    t4 = E58Twt.generate_timeSeries("users")
    
    with open("data/nyc-tweets-ts-201210-11.pickle", 'w') as fout:
        pickle.dump(t1, fout)
        pickle.dump(t2, fout)
        pickle.dump(t3, fout)
        pickle.dump(t4, fout)
    
    
    


if __name__ == '__main__':
    
    fname = "nyc-tweets-12"
    all_tweets = TweetGroup(fname="data/{0}.csv".format(fname))
    jacobTwt = all_tweets.filter_tweets_by_bbox(location['jacob'])
    plot_nycc_2012_jacob_case(jacobTwt)
    
#    find_tweets_measure_toMatch_traffic()
    
#    get_userCnt_TS()
    
