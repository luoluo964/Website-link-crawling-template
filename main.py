import requests
import parsel

#返回页面的全部代码
def get_http(myurl):
    #伪造的UA头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    response=requests.get(myurl,headers=headers)
    data=response.text
    data.encode("UTF-8")
    return data

#通过xpath得到需要的url
def get_url(data):
    #存储数据的列表
    dataList=[]
    urldata=parsel.Selector(data)
    #模糊匹配
    #这里是你的Xpath匹配规则
    XpathSelect='//*[contains(@id,"post")]/header/h2'
    parse_list=urldata.xpath(XpathSelect)
    for h in parse_list:
        #这里更进一步得到数据（最终数据）
        url=h.xpath("./a/@href").extract_first()
        dataList.append(url)
    return dataList

def download(list):
    #写入文件
    with open('urls.txt','w') as f:
        for url in list:
            f.write(str(url)+"\n")


#当前文件为启动文件
if __name__=="__main__":
    #这个列表将会收集全部的网页链接
    allUrl=[]
    #假设网页有11页，请根据情况修改
    for page in range(1,12):
        # 用{}预留一个接口，通过.format将页数进行传递
        #观察网站的翻页url变化，这里以page/1、page/2...为例
        base_url = "https://这是你的网页.com/page/{}/".format(page)
        #得到这一网页的源代码
        http=get_http(base_url)
        #得到源代码中的url
        urls=get_url(http)
        for url in urls:
            allUrl.append(str(url))
        #加个提示给控制台
        print("已经爬取完第"+str(page)+"页")
    #下载链接
    download(allUrl)
