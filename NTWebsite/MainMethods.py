from NTWebsite import AppConfig
from .improtFiles.models_import_head import *
from .Config import AppConfig as AC

#import AppConfig
#from models.Configuration import *

from NTWebsite.models.Configuration import *
from django.http import HttpResponse, HttpResponseRedirect
from django_redis import get_redis_connection
from redis import StrictRedis
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.core.cache import caches
#from oscrypto._win import symmetric
from oscrypto import symmetric
from PIL import Image as im
from NTConfig import settings
#from Crypto.Cipher import AES

import datetime
import hashlib
import base64
import os
import json
import re
import shutil
import sys
import time


def QueryRedisCache(MainBodyString, TimeOut=None, *Others):
    if TimeOut == None:
        TimeOut = AC().TimeOut

    CacheHandler = caches['default']
    '''
    sr = StrictRedis(host='localhost', port=1101, db=0)
    print(sys.getsizeof(sr))
    '''
    # 查询主体语句
    MainString = "\"" + MainBodyString + "\""
    # 生成复杂条件语句

    Others_Str_List = []
    Others_Obj_List = []
    if Others:
        for Other in Others:
            Others_Str_List.append("'%s'" % Other)
            Others_Obj_List.append("'Others[%d]'" % Others.index(Other))

        ObjectString = '(%s)' % (','.join(Others_Obj_List))
        # 因为_execCreate生成的变量名称都一样所以需要，获取实际变量值来生成MD5
        ObjectString_For_MD5 = '(%s)' % (','.join(Others_Str_List))
    else:
        ObjectString = '()'
        ObjectString_For_MD5 = '()'

    # 生成最终查询语句(变量名)
    FinalQueryString = eval(MainString + ' % ' + ObjectString)
    FinalQueryString_For_MD5 = eval(MainString + ' % ' + ObjectString_For_MD5)
    # 生成最终查询语句MD5码
    QueryString_MD5 = MD5(FinalQueryString_For_MD5)
    # 判断MD5是否存在，然后取数据
    if CacheHandler.get(QueryString_MD5) and TimeOut != 0:
        return CacheHandler.get(QueryString_MD5)
    else:
        try:
            print('查询语句(带变量值):', FinalQueryString_For_MD5)
            #print('查询语句(带变量名):', FinalQueryString)
            QueryResult = eval(FinalQueryString)
        except Exception as e:
            print('查询错误信息:', e) # 不直接raise Http404的原因是:部分get查询只是判断某些表中是否存在相应数据，不存在则忽略，不需要直接返回404
            #raise Http404
        else:
            CacheHandler.set(QueryString_MD5, QueryResult, TimeOut)
            return QueryResult


def PicUploadOperate(UploadedFile):
    APPConf = AC()
    # 返回json格式:{"uploaded":1,"fileName":"20170419091732.jpg","url":"/Upload/editor/20170419/20170419091732.jpg"}
    PicFormat = str(UploadedFile).split('.')[-1].lower()
    if PicFormat in APPConf.PicUploadFormat:
        PicUUID = str(uuid.uuid4())[-12:]
        PicSavePath = settings.MEDIA_ROOT + APPConf.PicTempPath
        PicSavePath_Preview = settings.MEDIA_URL + APPConf.PicTempPath
        PicSaveName = PicUUID + '.' + PicFormat
        if os.path.exists(PicSavePath) == False:
            os.makedirs(PicSavePath)
        SaveFullPath = PicSavePath + PicSaveName
        SaveFullPath_Preview = PicSavePath_Preview + PicSaveName
        with im.open(UploadedFile) as picHandle:
            W, H = picHandle.size
            temp_Pic = picHandle.resize(
                (APPConf.PicUploadWidth, int(H / W * APPConf.PicUploadWidth)), im.BILINEAR).convert('RGBA' if ImageFormat == 'png' else 'RGB')
            temp_Pic.save(SaveFullPath)
        return json.dumps({"uploaded": 1, "fileName": PicSaveName, "url": SaveFullPath_Preview}, ensure_ascii=False)
    else:
        return json.dumps({"uploaded": 0}, ensure_ascii=False)


def MovePicToSavePath(Content):
    APPConf = AC()
    result = re.findall("src=\"([^']+?)\"", Content)
    if os.path.exists(settings.MEDIA_ROOT + APPConf.PicSavePath) == False:
        os.makedirs(settings.MEDIA_ROOT + APPConf.PicSavePath)
    if result:
        for path in result:
            if APPConf.PicTempPath in path:
                shutil.move(settings.BASE_DIR + path,
                            settings.MEDIA_ROOT + APPConf.PicSavePath)
    NewContent = Content.replace(
        settings.MEDIA_URL + APPConf.PicTempPath, settings.MEDIA_URL + APPConf.PicSavePath)
    return NewContent


def RemovePicFromSavePath(TopicID, ContentUpdate):
    ContentOld = QueryRedisCache(
        'TopicInfo.objects.get(ObjectID=%s)', 0, TopicID).Content
    PathSet_Delete = set(re.findall(
        "src=\"([^']+?)\"", ContentOld)) - set(re.findall("src=\"([^']+?)\"", ContentUpdate))
    if PathSet_Delete:
        for path in PathSet_Delete:
            if os.path.exists(settings.APP_ROOT + path):
                os.remove(settings.APP_ROOT + path)


def UserAvatarOperation(ImageData, ImageFormat, OldAvatar):
    APPConf = AC()
    if ImageFormat != None and ImageFormat.upper() in APPConf.PicUploadFormat:
        savePath = os.path.join(settings.MEDIA_ROOT, APPConf.AvatarSavePath)
        saveFile = str(uuid.uuid1())[0:8] + '.' + ImageFormat
        saveFilePath = os.path.join(savePath, saveFile)

        if os.path.exists(savePath) == False:
            os.makedirs(savePath)
        try:
            with open(saveFilePath, 'wb') as picHandle:
                picHandle.write(base64.b64decode(ImageData.split('base64')[1]))

            with im.open(saveFilePath) as sizeHandle:
                compress_avatar = sizeHandle.resize(
                    (APPConf.AvatarResolution, APPConf.AvatarResolution), im.BILINEAR).convert('RGBA' if ImageFormat == 'png' else 'RGB')
                compress_avatar.save(saveFilePath)
            print("OldAvatar:",OldAvatar)
            print("asdadadasd:",APPConf.DefaultAvatar.url.replace(settings.MEDIA_URL,''))
            if OldAvatar != APPConf.DefaultAvatar.url.replace(settings.MEDIA_URL,''):
                if os.path.exists(os.path.join(settings.MEDIA_ROOT, OldAvatar)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, OldAvatar))
            return {'Status': 'success', 'Path': os.path.join(APPConf.AvatarSavePath, saveFile)}
        except Exception as e:
            return {'Status': e, 'Path': OldAvatar}
    else:
        return {'Status': 'invariant', 'Path': OldAvatar}


def Encrypt(data):
    APPConf = AC()
    return symmetric.aes_cbc_pkcs7_encrypt(APPConf.SecretKey.encode('utf-8'),
                                           data.encode('utf-8'),
                                           APPConf.SecretVI.encode('utf-8'))[1]


def Decrypt(data):
    APPConf = AC()
    return symmetric.aes_cbc_pkcs7_decrypt(APPConf.SecretKey.encode('utf-8'),
                                           data,
                                           APPConf.SecretVI.encode('utf-8')).decode('utf-8')


def EncodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64encode(data).decode()


def DecodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64decode(data)


def MD5(data):
    hash_md5 = hashlib.md5(data.encode('utf-8'))
    return hash_md5.hexdigest()


def GetUserIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']

def CounterOperate(object, field, method):
    exec("object.%s = F('%s')%s1" % (field, field, method))
    exec('object.save()')
    return exec('object.refresh_from_db()')

def CreateUUIDstr():
    return str(uuid.uuid4())[-12:]

if __name__ == "__main__":
    print('%s' % 'abc')
