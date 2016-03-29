import psycopg2


from matplotlib import get_backend
print get_backend()





def retrieve_data_from_db_server():
    """Retrieve all NYC tweets into local file"""
    
    conn = psycopg2.connect(host="lrs-jli02.ist.psu.edu", database="postgres", user="hxw186", password="hxw186")
    
    cur = conn.cursor()
    
    
    # the lon, lat is in NYC, the text contains hashtag
    cur.execute("""SELECT tweetid, userid, timestamp, lon, lat, text from usatweets where lat <= 40.87705 
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
                t = str(row[2])     # row[2] is the timestamp
                if t[0:6] == "201210":
                    fout12.write("{0},{1},{2},{3},{4},{5}\n".format(*row))
                elif t[0:6] == "201306":
                    fout13.write("{0},{1},{2},{3},{4},{5}\n".format(*row))
        


    
if __name__ == '__main__':
    
    retrieve_data_from_db_server()
