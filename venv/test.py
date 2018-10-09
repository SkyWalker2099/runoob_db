import urllib.request as url
import urllib
import pymysql
from bs4 import BeautifulSoup
import re
from lxml import etree
import jieba
import get_html
import get_QA


db = pymysql.connect(user = "zzh",
                     password = "123456",
                     host = "localhost",
                     db = "runoob")
cursor = db.cursor()

user_agent= 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {"User-Agent":user_agent, "Referer":"http://www.runoob.com/"}
#
#
proxy_handler = url.ProxyHandler({})
opener = url.build_opener(proxy_handler)
# # host = """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAA6ZJREFUWIXFlktsG1UYhb+58dgTj13bpG4TJ6WqQitSUEsQNCIg8ZCQUNmhKpuyqVggsUJiwwIR2ICABbBFiO4QLUJFVUHdQhseAZKWAg5phUjdxE4auzZ+j8d3WLg2E8WPSeOEs5rR/Pec8z/unasAHD45G9QMdVJaTAghImwtEhacLqvlycsnRtPK4ZOzQa3imQIObrHwGkhJ1PCUx4VmqJPbLQ4gBCPuiucNIS0mtlu8YQI54XLac7VH4fOJYQC+ms8wGy/w2uMDALx9Ic7ogJdn7gkA8Nxn15CWIwsDwqlbBej3qbw3leDr+TSxjIFQIJYxiN4sMXezRNjr4vzVjEPx2xach9bw/KE+xu/2sVN3UahIHh7UGQlr7PapZA3J8UN9CMU5n8tpoCktXj4fAyCRrZAumXzwwwoA88kyK3mThYwBgLWBCihjH/3RMrzP62KX7thjUyznTFJFs+X3tuxP7fPzynj/pgy8czHBmeitlt/bzkCyUN2UeI2jdfadDbQpnWMDHTjatsDeu5l4gU9mVhvvFrXRsQ9c/fHVxwbYG3Sv49iwAXv53D0KPy/l25LVodi2YacWtDVQqEhKpkRzCYbv8vD6ExGEAgoK0rL45u8s3y5kGwePVxUc3R9gt64CkDMkRrX9nuy4x1LFKhG/oNdVI18tmHwZvcWZuXQju70BN8fuC/HsgSBeVdjWdp6hjgaSBZOIv5bRuxcTnP0zjWk7ax/o93JkUCdnSE79lsLv6eHYwVBj7eYN2LKYTRTWiANcShS4lCg03g/0aQ0DXalAypbF0f0BlrKVpnHXUiWuLBcJ9fb8Z74bFbBn8eQ+Pyt5k36f2mhLHR/PrHJluUhQc9nWdj7IOv4NkzaSc/MZXjq3wKe/JtfF5cq1uJBmq0C3hrCOOvn0Yp6zc2nG9ugATC3k+D6WAyC4lS0I9dbCr2cM3roQbxq/tgVd3gVPD+9gzw4338VyTF3PMbdaxLLg3rDG2JCPR4Z07t/V23TtnRuwlVEBRsIaI2GNFx7cSbpU63vQ1vc6LJwNYUcDRtUib0h09/p5bSZcxz+lKlUHl0NH153jX/zFkSGdsUGdhyI6gRbC6VKVnxbzTC/mmb7h8MfV7krWDEKpnXY1Qz6kZTG9mOfHG3muJktsiOy2gTiwuXvXHUJKuSQsOP1/iAMIoZwSZbU8KSXRbVeX/G5a2pvi8onRtOEpj0v4EGTz06WbulIugfW+qXge/eXF4cy/C7eVCw87IhIAAAAASUVORK5CYII="""
# host = "http://www.runoob.com/html/html-tutorial.html"
# request = url.Request(host, headers=header)
# response = opener.open(request)
# # url.urlretrieve(host, "sss.png")
#
#
# print(response.read().decode("utf-8"))
# with open("sss.png" ,"wb") as f:
#     f.write(response.read())
#     f.close()







# html = """<div class="example_code">
# <a target="_blank" href="/try/try.php?filename=trycss_firstline_letter" class="tryitbtn">尝试一下 »</a>
# <div class="hl-main"><span class="hl-identifier">p</span><span class="hl-special">:first-letter</span><span class="hl-code">
# </span><span class="hl-brackets">{</span><span class="hl-code">
#     </span><span class="hl-reserved">color:</span><span class="hl-var">#ff0000</span><span class="hl-reserved"></span><span class="hl-code">;
#     </span><span class="hl-reserved">font-size:</span><span class="hl-string">xx-large</span><span class="hl-reserved"></span><span class="hl-code">;
# </span><span class="hl-brackets">}</span><span class="hl-code">
# </span><span class="hl-identifier">p</span><span class="hl-special">:first-line</span><span class="hl-code">
# </span><span class="hl-brackets">{</span><span class="hl-code">
#     </span><span class="hl-reserved">color:</span><span class="hl-var">#0000ff</span><span class="hl-reserved"></span><span class="hl-code">;
#     </span><span class="hl-reserved">font-variant:</span><span class="hl-string">small-caps</span><span class="hl-reserved"></span><span class="hl-code">;
# </span><span class="hl-brackets">}</span></div>
# </div>"""
#
#
#
# p = re.compile(r'<a .*>')
# html = p.sub("", html)
#
# print(html)






# host = "http://www.runoob.com/mysql/mysql-handling-duplicates.html"
# resquest = url.Request(host, headers=header)
# response = opener.open(resquest)
#
#
# text = response.read().decode('utf-8')
#
# xpath = """//*[@id="content"]"""
# html = etree.HTML(text)
# a = html.xpath(xpath)
#
#
# a = BeautifulSoup(etree.tostring(a[0]))
# # print(str(a))
# a = a.find(name="div", attrs={"class":"article-intro","id":"content"})
# print(str(a))

sql = """select * from href_list where id = 2534;"""
cursor.execute(sql)
result = cursor.fetchall()[0]
print(result[1])
html = get_html.get_html(result[1])

qa = get_QA.f(result)

# for i in qa:
#     print(i)





