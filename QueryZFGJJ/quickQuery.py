#coding:cp936
import urllib,os,urllib2,cookielib,socket
import Image,pytesser
import re,time,thread
#szgjj_url="http://www.szzfgjj.com/fzgn/zfcq/"



def identifyCode(codename):
    # 二值化
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    im=Image.open(codename)
    imgry = im.convert('L')
    imgry.save('g'+codename)
    out = imgry.point(table,'1')
    out.save('b'+codename)
    os.chdir("D:\\Python27\\Lib\\site-packages\\pytesser_v0.0.1")
    text=pytesser.image_to_string(out)
    return text


def Requestszgjj(gjj_account,id_num,codename):
    #POST请求，返回response.read()
    szgjj_url="http://app.szzfgjj.com:7001/accountQuery"
    verifycode="http://app.szzfgjj.com:7001/pages/code.jsp"
    gjj_account_html='accnum'
    id_html="certinum"
    verify_html='verify'
    qryflag='qryflag'
    #codename="code.gif"

    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        }

    picture = opener.open(verifycode).read()
    local = open(codename, 'wb')
    local.write(picture)
    local.close()
    v_code=identifyCode(codename).strip()
    post_data={gjj_account_html:gjj_account,id_html:id_num,verify_html:v_code,qryflag:1}
    #print post_data
    data = urllib.urlencode(post_data)
    request = urllib2.Request(szgjj_url, data, headers)
    response = opener.open(request)
    #print dir(response)
    result = response.read().decode('UTF8')
    return result

def resultFilter(strings):
    #返回response的结果,true or false
    #strings =Requestszgjj()
    suceess_if_patten=re.compile("success:(.*?)\,")
    success_if=suceess_if_patten.findall(strings)[0]
    if success_if=='true':
        return True
    elif success_if=='false':
        return False

def Displayresult(strings,success):
    #根据response  的true  or false，来显示结果
    #strings =Requestszgjj()
    newaccnum_patten=re.compile("newaccnum:\'(.*?)\'\,")
    msg_patten=re.compile("msg:\'(.*?)\'\,")
    sbbalance_patten=re.compile("sbbalance:\'(.*)\'")
    cardstat_patten=re.compile("cardstat:\'(.*?)\'\,")
    gjj_money=msg_patten.findall(strings)[0]
    display_string=''
    if success:
        newaccnum_number=newaccnum_patten.findall(strings)[0]
        sbbalance_money=sbbalance_patten.findall(strings)[0]
        cardsta=cardstat_patten.findall(strings)[0]
        dstring=u'公积金账号：%s 公积金金额：%s 社保移交金额：%s 卡状态：'% (newaccnum_number,gjj_money,sbbalance_money)
        display_string+=dstring
        if cardsta=='2':
            display_string+=u"正常"
        else:
            display_string+=u"不正常"
    else:
        display_string=u"提示: %s  将自动进行下次查询，需要修改信息，请关闭程序" %gjj_money
    return display_string


if __name__=="__main__":
    #公积金账号，数字
    #gjj_account=******************
    #身份证号，数字
    #id_num=*******************
    socket.setdefaulttimeout(5.0)
    def querystartat(gjj_account,id_num,codename,times=1):#times支持从当前公积金好开始查询多少个
        orign_end=gjj_account+times
        if_continue=True
        while if_continue and (gjj_account<orign_end):
            try:
                print "公积金账号：",gjj_account
                request_rst=Requestszgjj(gjj_account,id_num,codename)
                if_success=resultFilter(request_rst)
                time.sleep(0.3)
                responeTXT=Displayresult(request_rst,if_success)
                gjj_account+=1
                if if_success:
                    print responeTXT
                    if_continue=False
                else:
                    if u'验证码错误' in responeTXT:
                        print responeTXT
                        gjj_account=gjj_account-1
                    else:
                        print responeTXT
            except Exception as e:
                print e
    querystartat(20325923771,430726198911151810,"code2.gif")
