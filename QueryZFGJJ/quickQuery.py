#coding:cp936
import urllib,os,urllib2,cookielib
import Image,pytesser
import re,time

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


def Requestszgjj(gjj_account,id_num):
    szgjj_url="http://app.szzfgjj.com:7001/accountQuery"
    verifycode="http://app.szzfgjj.com:7001/pages/code.jsp"
    gjj_account_html='accnum'
    id_html="certinum"
    verify_html='verify'
    qryflag='qryflag'
    codename="code.gif"
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
    suceess_if_patten=re.compile("success:(.*?)\,")
    success_if=suceess_if_patten.findall(strings)[0]
    if success_if=='true':
        return True
    elif success_if=='false':
        return False

def Displayresult(strings,success):
    newaccnum_patten=re.compile("newaccnum:\'(.*?)\'\,")
    msg_patten=re.compile("msg:\'(.*?)\'\,")
    sbbalance_patten=re.compile("sbbalance:\'(.*)\'")
    cardstat_patten=re.compile("cardstat:\'(.*?)\'\,")
    gjj_money=msg_patten.findall(strings)[0]
    if success:
        newaccnum_number=newaccnum_patten.findall(strings)[0]
        sbbalance_money=sbbalance_patten.findall(strings)[0]
        cardsta=cardstat_patten.findall(strings)[0]
        print '公积金账号：',newaccnum_number,
        print '公积金账号：',gjj_money,
        print '社保移交金额：',sbbalance_money,
        if cardsta=='2':
            print '卡状态：正常'
        else:
            print "卡状态：不正常"
    else:
        print "msg:",gjj_money,"将自动进行下次查询，需要修改信息，请关闭程序"


if __name__=="__main__":
    #公积金账号，数字
    gjj_account= ************
    #身份证号，数字
    id_num= ************

    if_continue=True
    while if_continue:
        request_rst=Requestszgjj(gjj_account,id_num)
        if_success=resultFilter(request_rst)
        time.sleep(2)
        if if_success:
            Displayresult(request_rst,if_success)
            if_continue=False
        else:
            Displayresult(request_rst,if_success)


