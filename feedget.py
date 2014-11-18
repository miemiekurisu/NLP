import feedparser
import re

feed1 = feedparser.parse('http://cn.engadget.com/rss.xml')
#print feed1['entries'] #.decode('utf-8')
lent = len(feed1['entries'])
for i in range(0, lent):
    feedcontent = feed1['entries'][i]['summary'].encode('utf-8').decode('utf-8')
    magica = re.search('\<.*\/\>',feedcontent)
    print '%r Time-%r: '%(i,feed1['entries'][i]['published']) + feedcontent[:magica.start()]+feedcontent[magica.end():]