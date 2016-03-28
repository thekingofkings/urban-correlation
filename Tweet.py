"""
Hongjian
3/26/2016


Factor the Tweet class into one file
"""



from pre_processing_function import date2linux_timestamp
import re


class Tweet:
    
    hist_hashtag = {}
    
    
    def __init__(self, tid, timestamp, lon, lat, text):
        self.tid = int(tid)
        self.timestamp = timestamp
        self.timestamp += "0" * (17 - len(self.timestamp))    # fix all timestamp length as 17
        self.lon = float(lon)
        self.lat = float(lat)
        self.text = text.strip()
        tags = re.findall("#\w+", self.text)
        self.hashtag = [s.lower() for s in tags]
        
    
    def __str__(self):
        """override __str__ for output"""
        return "{0},{1},{2},{3},{4}".format(self.tid, self.timestamp, self.lon, self.lat, self.text)
        
        
        
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
            
            
    def location_key(self):
        return "{0:0.3f}{1:0.3f}".format(self.lon, self.lat)