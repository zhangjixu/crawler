#-*- encoding: gb2312 -*-
# @Time    : 2018/8/7 15:44
# @Author  : zhangjixu
# _*_ coding=gb2312 _*_
import email

fp = open("D:\\chen.eml", "r")
msg = email.message_from_file(fp)

if __name__ == '__main__':
    # ѭ���ż��е�ÿһ��mime�����ݿ�
    for par in msg.walk():
        if not par.is_multipart():  # ����Ҫ�ж��Ƿ���multipart���ǵĻ�����������������õģ�����Ϊʲô�����˽�mime���֪ʶ��
            name = par.get_param("name")  # ����Ǹ���������ͻ�ȡ���������ļ���
            if name:
                # �и���
                # ��������д���ֻ��Ϊ�˽�����=?gbk?Q?=CF=E0=C6=AC.rar?=�������ļ���
                h = email.Header.Header(name)
                dh = email.Header.decode_header(h)
                fname = dh[0][0]
                print('������:', fname)
                data = par.get_payload(decode=True)  # ������������ݣ�Ȼ��洢���ļ���
                print(data)
                try:
                    f = open(fname, 'wb')  # ע��һ��Ҫ��wb�����ļ�����Ϊ����һ�㶼�Ƕ������ļ�
                except:
                    print('�������зǷ��ַ����Զ���һ��')
                    f = open('aaaa', 'wb')
                f.write(data)
                f.close()
            else:
                # ���Ǹ��������ı�����
                print(par.get_payload(decode=True)) # ������ı����ݣ�ֱ��������Ϳ����ˡ�
