import urllib2
from sgmllib import SGMLParser

class ListName(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_h5=""
        self.name=[]
    def start_h5(self,attrs):
        self.is_h5=1
    def end_h5(self):
        self.is_h5=""
    def handle_data(self,text):
        if self.is_h5==1:
            self.name.append(text)

content = urllib2.urlopen('http://list.taobao.com/browse/cat-0.htm').read()
listname = ListName()
listname.feed(content)
for item in listname.name:
    print item.decode('gbk').encode('utf8')

