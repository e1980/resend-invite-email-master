# coding=utf-8
import pymssql
import requests
import json

receptions = [
    {'tentant': 'alp7', 'email': 'zhou.jiaxuan@siemens.com'},
    {'tentant': 'alp7', 'email': 'pinghu@siemens.com'},
    {'tentant': 'alp7', 'email': 'chun.lu@siemens.com'},
]




def send_email(token,email,tentant,locale,sp_alias_name):
    tentant_link = "https://" + tentant + '.cn1.mindsphere-in.cn'
    param={
        "tenantLink":tentant_link,
        "locale":locale,
        "spAliasName":sp_alias_name
    }
    header={"Authorization":"Bearer "+token}
    r=requests.post("https://webkey.cn1.mindsphere-in.cn/wks/webkeyrest/external/v1/users/"+email+"/invite/",
                    json=param,headers=header)

def get_alias(cursor,tentant):
    sql = 'select SP_ALIAS_NAME from SAML_CONFIGURATION where AUDIENCE=\'' + tentant + '.uiam.cn1.mindsphere-in.cn\''
    cursor.execute(sql)
    # 用一个rs变量获取数据
    rs = cursor.fetchall()
    alias = rs[0][0]
    return alias


def resend(cursor,token,tentant,email):
    alias=get_alias(cursor,tentant)
    send_email(token,email,tentant,'zh',alias)
    print("send email to "+ email + 'for tentant '+tentant+'. SP alias is ' + tentant+'.')

def get_token():
    param={
        'audience': 'https://sws.siemens.com',
        'client_id': 'BcRWoRBXP44EFhrD7zRutVvOTUB1sQ3y',
        'client_secret': 'pe8aHDCyw4GKb2sY5sjku5W4Je_EFuZEsEd1D2Y58-ZlzOq2NOnQ8v_NXcJmztGn',
        'grant_type': 'client_credentials'
    }
    r=requests.post("https://splm.auth0.com/oauth/token",data=param)
    token=json.loads (r.content)['access_token']
    print("get token :"+ token)
    return token

if __name__ == '__main__':
    conn = pymssql.connect(host='rm-uf6355zu7lpaa5z530o.sqlserver.rds.aliyuncs.com',
                           user='webkeyadmin1',
                           password='Wk19Wk19',
                           database='webkey',
                           charset='utf8')
    cursor = conn.cursor()
    token=get_token()
    for reception in receptions:
        resend(cursor,token,reception['tentant'],reception['email'])







