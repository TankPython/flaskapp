#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8a216da85fe1c856015ff72291c50994'

#���ʺ�Token
accountToken= '5bb4050e66a6445f8f9ff271ff5927d6'

#Ӧ��Id
appId='8a216da85fe1c856015ff7229225099b'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿�
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id
class CCP(object):

    instance = None

    def __new__(cls):
        if not cls.instance:
            object = super(CCP,cls).__new__(cls)
            # ��ʼ��REST SDK
            object.rest = REST(serverIP, serverPort, softVersion)
            object.rest.setAccount(accountSid, accountToken)
            object.rest.setAppId(appId)

            cls.instance = object

        return cls.instance

    def send_template_sms(self,to,datas,tempId):

        result = self.rest.sendTemplateSMS(to,datas,tempId)

        statusCode = result.get("statusCode")
        if statusCode == "000000":
            return "1"
        else:
            return "0"
        # for k,v in result.iteritems():
        #
        #     if k=='templateSMS' :
        #             for k,s in v.iteritems():
        #                 print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)


ccp = CCP()
# ret = ccp.send_template_sms("15813370410", ["1234", "5"], 1)
# print ret


