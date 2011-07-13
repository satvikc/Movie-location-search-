from scrapy.selector import HtmlXPathSelector
from scrapy.http import HtmlResponse
import json,pdb,sys
import httplib
baseurl="http://www.google.com/movies?near="

def search(city,date):
    movielist=[]
    start=0

    conn = httplib.HTTPConnection("www.google.com")
    conn.request("GET", "/movies?near="+city+"&start="+str(start)+"&date="+str(date))
    r1=conn.getresponse()
    hxs=HtmlXPathSelector(HtmlResponse("www.google.com/movies?near="+city+"&date="+str(date)+"&start="+str(start),r1.status,r1.getheaders(),r1.read(),request=conn))
    st=hxs.extract()
    while("No showtimes were found" not in st):
        theater=hxs.select('//h2[contains(@class,"name")]/a[contains(@href,"movies")]/text()').extract()
        m=hxs.select('//div[contains(@class,"name")]/a[contains(@href,"movies")]/text()').extract()
        x=hxs.select('//div[contains(@class,"times")]/text()').extract()
        counter=0
        for i,j in zip(theater,theater[1:]):
            star=st.find(i)
            end=st.find(j)
            test=st.find(m[counter],star,end)
            while(test!=-1):
                temp=x[counter].split()
                try:
                    am=next(temp1 for temp1,temp2 in enumerate(temp) if temp2.endswith("am"))
                    temp[am]=temp[am][:-2]
                except:
                    am=0
                try:
                    pm=next(temp1 for temp1,temp2 in enumerate(temp) if temp2.endswith("pm"))
                    temp[pm]=temp[pm][:-2]
                    for temp3 in range(am+1,pm+1):
                        if int(temp[temp3].split(':')[0])<12:
                            temp[temp3]=str((int(temp[temp3].split(':')[0])+12)%24)+temp[temp3][temp[temp3].find(':'):]
                except:
                    pass
                movielist.append((i,m[counter],temp))

                star =test+len(m[counter])
                counter+=1
                test=st.find(m[counter],star,end)
        while(counter!=len(m)):
            temp=x[counter].split()
            try:
                am=next(temp1 for temp1,temp2 in enumerate(temp) if temp2.endswith("am"))
                temp[am]=temp[am][:-2]
            except:
                am=0
            try:
                pm=next(temp1 for temp1,temp2 in enumerate(temp) if temp2.endswith("pm"))
                temp[pm]=temp[pm][:-2]
                for temp3 in range(am+1,pm+1):
                    if int(temp[temp3].split(':')[0])<12:
                        temp[temp3]=str((int(temp[temp3].split(':')[0])+12)%24)+temp[temp3][temp[temp3].find(':'):]
            except:
                pass
            movielist.append((theater[-1],m[counter],temp))
            counter+=1
        #pdb.set_trace()
        conn.close()
        start+=10
        conn = httplib.HTTPConnection("www.google.com")
        conn.request("GET", "/movies?near="+city+"&start="+str(start)+"&date="+str(date))
        r1=conn.getresponse()
        hxs=HtmlXPathSelector(HtmlResponse("www.google.com/movies?near="+city+"&date="+str(date)+"&start="+str(start),r1.status,r1.getheaders(),r1.read(),request=conn))
        st=hxs.extract()
    #return json.JSONEncoder().encode(movielist)
    return json.dumps(movielist, sort_keys=True, indent=4)
if __name__ == "__main__":
    if len(sys.argv)>1:
        m=search(sys.argv[1],0)
    else:
        m=search('kanpur',0)
    print m
    
