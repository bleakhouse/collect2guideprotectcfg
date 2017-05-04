# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import json
import logging
import logging.handlers
import platform
import thread
import time
import urllib2
import platform

import os
import traceback

# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import sys
import thread
import time
import logging
import traceback
import logging.handlers
import urllib2
import urllib
import json
import mylogging
import MySQLdb


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

DATABASE_NAME  = 'guideprotect'


def pretty_xmlfile(fname):
    from lxml import etree as ET
    parser = ET.XMLParser(
        remove_blank_text=False, resolve_entities=True, strip_cdata=True)
    xmlfile = ET.parse(fname, parser)
    pretty_xml = ET.tostring(
        xmlfile, encoding = 'UTF-8', xml_declaration = True, pretty_print = True)
    file = open(fname, "w")
    file.writelines(pretty_xml)
    file.close()

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i


def getDbOrCreate(dbname=DATABASE_NAME):

    obj=None
    op = None
    try:

        obj = MySQLdb.connect("127.0.0.1","test","123456",  charset="utf8")

        obj.autocommit(1)
        op = obj.cursor()

        op.execute("use "+dbname)
    except Exception, e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
    return  op

from basedef import *

def dumpsql2xml(fname='new_rule'):

    fname = fname+time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time()))+".xml"
    if os.path.isfile(fname):
        inp = raw_input('file {0} existed, ok to overwrite ? press 1 to continue\n'.format(fname))

        if not inp.isdigit():
            return

        if (int)(inp) != 1:
            return


    dbobj = getDbOrCreate()
    number = dbobj.execute('select * from forgeurls')
    if number==0:
        print 'there is no records in database'
        return
    result = dbobj.fetchall()

    rule={}

    doc = ET.Element('doc')
    doc.attrib['version'] = '1.0'

    for row in result:
        url = row[3]

        rule[RULE_ATTR_NAME_name] = "safe navigate"
        rule[RULE_ATTR_NAME_host] = ""
        rule[RULE_ATTR_NAME_redirect_type] = RULE_ATTR_NAME_redirect_type_file
        rule[RULE_ATTR_NAME_req] = ""
        rule[RULE_ATTR_NAME_redirect_target] = "safe_navigate.html"
        rule[RULE_ATTR_NAME_req_match_method] = RULE_ATTR_NAME_req_match_method_same
        rule[RULE_ATTR_NAME_full_url] = url

        rulenode = ET.SubElement(doc,RULE_ATTR_NAME_rule)
        rulenode.attrib[RULE_ATTR_NAME_name] = rule[RULE_ATTR_NAME_name]

        host            = ET.SubElement(rulenode, RULE_ATTR_NAME_host)
        redirect_type   = ET.SubElement(rulenode, RULE_ATTR_NAME_redirect_type)
        req             = ET.SubElement(rulenode, RULE_ATTR_NAME_req)
        redirect_target = ET.SubElement(rulenode, RULE_ATTR_NAME_redirect_target)
        req_match_method = ET.SubElement(rulenode, RULE_ATTR_NAME_req_match_method)
        full_url = ET.SubElement(rulenode, RULE_ATTR_NAME_full_url)

        host.text           = rule[RULE_ATTR_NAME_host]
        redirect_type.text  = rule[RULE_ATTR_NAME_redirect_type]
        req.text            = rule[RULE_ATTR_NAME_req]
        redirect_target.text = rule[RULE_ATTR_NAME_redirect_target]
        req_match_method.text = rule[RULE_ATTR_NAME_req_match_method]
        full_url.text = rule[RULE_ATTR_NAME_full_url]



    tree = ET.ElementTree(doc)
    tree.write(fname, encoding="UTF-8")
    pretty_xmlfile(fname)
    print '\n\n'

import sys
if __name__=='__main__':

    try:

        dumpsql2xml()
    except Exception, e:
        logging.error(str(e))
        logging.error(traceback.format_exc())

    raw_input('press anykey to exit!\n')
