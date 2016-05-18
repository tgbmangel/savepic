#coding:cp936
#深圳公积金查询
import urllib,os,urllib2,cookielib
import Image,pytesser
import re,time
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


def Requestszgjj(gjj_account,id_num):
    #POST请求，返回response.read()
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
    #返回response的结果,true or false
    suceess_if_patten=re.compile("success:(.*?)\,")
    success_if=suceess_if_patten.findall(strings)[0]
    if success_if=='true':
        return True
    elif success_if=='false':
        return False

def Displayresult(strings,success):
    #根据response  的true  or false，来显示结果
    #print strings
    #{success:false,msg:'验证码错误',oppsucc:false}
    #{success:true,cardstat:'2',newaccnum:'20325923777',msg:'14984.03',peraccstate:'0',oppsucc:false,sbbalance:'0.00'}
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
        display_string+=u'公积金账号： 公积金金额：社保移交金额：卡状态： \n'
        display_string+=newaccnum_number
        display_string+=gjj_money
        display_string+=sbbalance_money
        if cardsta=='2':
            display_string+=u"正常"
        else:
            display_string+=u"不正常"
    else:
        display_string+=gjj_money
        display_string+=u"  将自动进行下次查询，需要修改信息，请关闭程序"
    return display_string


if __name__=="__main__":
    #公积金账号遍历起始位置
    gjj_account=***********
    #身份证号，数字
    id_num=******************
    while True:
        try:
            gjj_account+=1
            print "公积金账号：",gjj_account
            if_continue=True
            request_rst=Requestszgjj(gjj_account,id_num)
            if_success=resultFilter(request_rst)
            time.sleep(0.3)
            responeTXT=Displayresult(request_rst,if_success)
            if if_success:
                print responeTXT
                break
            else:
                if u'验证码错误' in responeTXT:
                    print responeTXT
                    gjj_account=gjj_account-1
                else:
                    print responeTXT
        except Exception as e:
            print e


