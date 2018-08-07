# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 15:35
# @Author  : zhangjixu

import datetime
import json
import eml_parser


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


if __name__ == '__main__':

    subject = eml_parser.eml_parser.decode_email("D:\\chen.eml")
    print(subject)

    with open('D:\\chen.eml', 'rb') as fhdl:
        raw_email = fhdl.read()
    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)
    json_serial(parsed_eml)
    print(json.dumps(parsed_eml, default=json_serial))