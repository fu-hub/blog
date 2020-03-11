import requests
import time
import PIL.Image as Image
import os
from bs4 import BeautifulSoup
import re



def locationSearch(locationName):
    city = "武汉"
#    locationName = "武汉大学"
    resultBuf = []
    searchAPI = "http://api.map.baidu.com/place/v2/suggestion?query=" \
                + locationName + "&region=" + city + \
                "&city_limit=true&output=json&ak=pfpPI4QukKfMuGif6gvqjLvo3qnGhKor"
    try:
        jsonResult = requests.get(searchAPI, timeout=20).json()
        #    print(jsonResult)
        if "result" in jsonResult.keys():
            searchResult = jsonResult["result"]
            print("备选地点:")
            i = 1
            for eachResult in searchResult:
                print(eachResult.setdefault('location',0))
                if eachResult['location']==0:
                    return 0
                print('%d.' %i + eachResult["name"], "纬度", eachResult["location"]["lat"], "经度",
                  eachResult["location"]["lng"])
                resultBuf.append(eachResult["name"] + " " + str(eachResult["location"]["lat"]) + \
                             " " + str(eachResult["location"]["lng"]))
                i = i+1
    except requests.exceptions.ChunkedEncodingError:
        print('ChunkedEncodingError')
    except requests.exceptions.ConnectTimeout:
        print('ConnectTimeout')
    except requests.ReadTimeout:
        print('ReadTimeout') 
    except OSError:
        pass       
    return resultBuf


try:
    def baiduPanoramicMap(localPath, name, latitude, longitude):
            if not os.path.exists(localPath):# 新建文件夹
                os.mkdir(localPath)
            pitch = 0
            area = 120
            stride = 20
            num = 12
            panoramicMapAPI = "http://api.map.baidu.com/panorama/v2?ak=pfpPI4QukKfMuGif6gvqjLvo3qnGhKor" \
                      "&width=1024&height=512&location=" + str(longitude) + "," + str(latitude)\
                      +"&pitch="+str(-pitch)+"&fov="+str(area)
            for i in range(num):
                 try:
                     ir = requests.get(panoramicMapAPI + "&heading=%d" %(i*stride),timeout=7)
                     print(panoramicMapAPI + "&heading=%d" %(i*stride))
                 except requests.exceptions.ChunkedEncodingError:
                     print('ChunkedEncodingError')
                 except requests.exceptions.ConnectTimeout:
                     print('ConnectTimeout')
                 except requests.ReadTimeout:
                     print('ReadTimeout')
#        imgPath = localPath + '/' + name + '_' + latitude + '_' + longitude + '_%d.jpg' %(i+1)
                 open(localPath + '/' + name + '_' + latitude + '_' + longitude + str(pitch) + '_%d.jpg' %(i+1), 'wb').write(ir.content)
                 ir.close()
                 time.sleep(0.1)
 #       imgPath = imgPath.replace("/", "\\")
 #       img = Image.open(imgPath) 
 #       stitchedImg.paste(img, (i*1024, 0))
 #       stitchedImg.save(localPath + '\\' + name + '_' + latitude + '_' + longitude + '.jpg')
 #       os.remove(imgPath)

            print('下载完成')
except requests.exceptions.ChunkedEncodingError:
                     print('ChunkedEncodingError')
except requests.exceptions.ConnectTimeout:
                     print('ConnectTimeout')
except requests.ReadTimeout:
                     print('ReadTimeout')  
except OSError:
    pass

def toursearch(cityname):
    t=0
    r=requests.get("http://"+cityname+".mipang.com/jingdian/",timeout=30)
    html=r.text
    soup=BeautifulSoup(html,"lxml")
    title = soup.select('div > ul.clearfix > li > a ')
    new_data = []
    p = re.compile(r'[\u4e00-\u9fa5]')
    for i in range(len(title)):
        data = re.findall(p, str(title[i])) 
        result = ''.join(data)
        if result.find(u"爱米胖") !=-1:
            t=1
            continue
        if t==1:
            if result.find(u"景点") !=-1:
                 break
            new_data.append(result)
    box = []
    for i in range(len(new_data)-2):
        if new_data[i] != '':
            box.append(new_data[i+2])
    return box
def hospitalsearch():
    t=0
    kv={'user-agent':'Mozilla/5.0'}
    r=requests.get("https://www.haodf.com/yiyuan/guangdong/list.htm",headers=kv,timeout=30)
    r.encoding=r.apparent_encoding
    r.raise_for_status
    html=r.text
    soup=BeautifulSoup(html,"html.parser")
    title = soup.select('div > ul > li > a ')
    new_data = []
    p = re.compile(r'[\u4e00-\u9fa5]')
    for i in range(len(title)):
        data = re.findall(p, str(title[i])) 
        result = ''.join(data)
        if result.find(u"广州市老人院") !=-1:
            t=1
            continue
        if t==1:
            if result.find(u"佛山市第一人民医院 ") !=-1:
                break
            new_data.append(result)
    box = []
    for i in range(len(new_data)):
        if new_data[i] != '':
            box.append(new_data[i])
    return box
def collegesearch():
    t=0
    kv={'user-agent':'Mozilla/5.0'}
    r=requests.get("https://www.dxsbb.com/news/1683.html",headers=kv,timeout=30)
    r.encoding=r.apparent_encoding
    r.raise_for_status
    html=r.text
    soup=BeautifulSoup(html,"html.parser")
    title = soup.select('tbody > tr > td ')
    new_data = []
    p = re.compile(r'[\u4e00-\u9fa5]')
    for i in range(len(title)):
        data = re.findall(p, str(title[i])) 
        result = ''.join(data)
        if result.find(u"备注") !=-1:
            t=1
            continue
        if t==1:
            if result.find(u"学院") !=-1 or result.find(u"大学") !=-1:
                new_data.append(result)
    box = []
    for i in range(len(new_data)):
        if new_data[i] != '':
            box.append(new_data[i])
    return box
def stationsearch(cityname):
    kv={'user-agent':'Mozilla/5.0'}
    r=requests.get("http://www.piaojia.cn/"+cityname+"/changtu.html",headers=kv,timeout=30)
    r.encoding=r.apparent_encoding
    r.raise_for_status
    html=r.text
    soup=BeautifulSoup(html,"lxml")
    title = soup.select('tr > td > a ')
    new_data = []
    p = re.compile(r'[\u4e00-\u9fa5]')
    for i in range(len(title)):
        data = re.findall(p, str(title[i])) 
        result = ''.join(data)
        if result.find(u"客运") !=-1:
            new_data.append(result)
    box = []
    for i in range(len(new_data)):
        if new_data[i] != '':
            box.append(new_data[i])
    return box

if __name__ == '__main__':
    tourist=toursearch('wuhan')
    for i in tourist:
        if locationSearch(i)==0:
                continue
        for j in range(len(locationSearch(i))):
            try:
                cityInfo = locationSearch(i)[j].split()
                print(cityInfo)
                #保存地址需要自己修改
                baiduPanoramicMap('D:/depict', cityInfo[0], cityInfo[1],cityInfo[2])
                print(j)
            except requests.exceptions.ChunkedEncodingError:
                     print('ChunkedEncodingError')
            except requests.exceptions.ConnectTimeout:
                     print('ConnectTimeout')
            except requests.ReadTimeout:
                     print('ReadTimeout') 
            except OSError:
                pass
            continue