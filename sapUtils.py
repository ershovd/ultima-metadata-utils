# -*- coding: utf-8 -*-
# Utils for working with SAP SOAP stuff

from find import getTreeRoot

def printGoodsID(filename):
    _printStuff(filename, 1, '{urn://ulmart.ru/pi/ULTIMA.ERP}goodsTransferItems', ',')

def printBarCodes(filename):
    _printStuff(filename, 0, '{urn://ulmart.ru/pi/ULTIMA.ERP}barcodesTransferItems')

def _printStuff(filename, itemIndex, itemsTag, tail=''):
    for child in getTreeRoot(filename):
        if child.tag == '{http://www.w3.org/2003/05/soap-envelope}Body':
            for docSpec in child[0]:
                if docSpec.tag == itemsTag:
                    for good in docSpec:
                        print str(good[itemIndex].text) + tail


printBarCodes('NotEnoughGoods.xml')