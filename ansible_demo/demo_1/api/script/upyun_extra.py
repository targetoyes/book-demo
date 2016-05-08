#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import upyun
from functools import wraps
#up = upyun.UpYun('testjj01', 'test1', 'targetoyes123', timeout=30, endpoint=upyun.ED_AUTO)

def Up_Common(x=''):
    def Up_Deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print x
                return func(*args, **kwargs)
            except upyun.UpYunServiceException as se:
                Err = {'Error': 'Except an UpYunServiceException'}
                Id = {'Request_Id': se.request_id}
                Code = {'HTTP_Status_Code': str(se.status)}
                Mes = {'Message': se.msg}
                msgs = [Err, Id, Code, Mes]
                return msgs
            except upyun.UpYunClientException as ce:
                Err = {'Error': 'Except an UpYunClientException'}
                Id = {'Request_Id': ''}
                Code = {'HTTP_Status_Code': ''}
                Mes = {'Message': ce.msg}
                msgs = [Err, Id, Code, Mes]
                return msgs
        return wrapper
    return Up_Deco

class Upyun_Api(object):

    def __init__(self, bucket, username, passwd, timeout=30, endpoint=upyun.ED_AUTO):
        self.up = upyun.UpYun(bucket,
                            username,
                            passwd,
                            timeout=timeout,
                            endpoint=endpoint)

    @Up_Common('创建目录')
    def mkdir(self, new_dir):
        return self.up.mkdir(new_dir)

    @Up_Common('显示目录')
    def getlist(self, direc):
        return self.up.getlist(direc)

    @Up_Common('文件信息')
    def getinfo(self, filename):
        return self.up.getinfo(filename)

    @Up_Common('空间情况')
    def usage(self):
        return self.up.usage()

    @Up_Common('文件删除')
    def delete(self, direc):
        try:
            self.up.delete(direc)
        except Exception,e:
            return e

    @Up_Common('上传文件')
    def put(self, yun_file, file_body):
        res = self.up.put(yun_file, file_body)
        return res

    @Up_Common('获取资源')
    def get(self, yun_file, local_file):
        with open(local_file, 'wb') as f:
            res = self.up.get(yun_file, f)
        return res






if __name__ == '__main__':
    up = Upyun_Api('testjj01', 'test1', 'targetoyes123')
    print up.getlist('/')
    print up.usage()
    print up.getinfo('/temp1/test1.file')
    print up.mkdir('/temp1')
    print up.put('/temp1/test.file', '/temp/upyun_test/test.file')
    print up.get('/temp1/test.file', '/temp/upyun_test/test.file2')

#with open('/temp/upyun_test/test.file', 'rb') as f:
#    res = up.put('/temp/test.file', f, checksum=True)

#up.mkdir('/temp/')

#print up.getlist('/temp')
#res = up.usage()
#print res
