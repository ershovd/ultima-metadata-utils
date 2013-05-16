# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


#getTreeRoot('Metadata.xmd'):

_types_map = {
    "System.Int64": "long",
    "System.String": "string",
    "System.Boolean": "bool",
    "System.Decimal": "decimal",
    "System.DateTime": "datetime",
    "System.Int32": "int",
    "System.UInt32": "uint",
    "System.Byte[]": "byte[]"
}

class ToOneRefElement:
    ID = None
    Caption = None
    Property = None
    Dictionary = None

    def __str__(self):
        return u'   {0} = {1} Справочник: {2}, Свойство: {3}'.format(self.Caption, self.ID, self.Dictionary, self.Property)


class PropertyElement:
    ID = None
    Caption = None
    Type = None
    DBColumn = None
    Required = False
    Persistent = True
    DisplayKey = False

    def _shortType(self):
            if _types_map.has_key(self.Type):
                return  _types_map[self.Type]
            else:
                return self.Type

    def __str__(self):
        return u'    {0} = {1} ({2})'.format(self.Caption, self.ID, self._shortType())


class DictionaryDesc:
    ID = None
    Name = None
    DBtable = None
    Caption = None
    DBID = None

    def __str__(self):
        return u'Справочник: {0} ({1}), Таблица: {2} ({3})'.format(self.Caption, self.Name, self.DBtable, self.DBID)


class DictionaryElement:
    Description = None
    Properties = list()
    ToOneRefs = list()
    ToManyRefs = list()

    def _printToOneRefs(self):
        if len(self.ToOneRefs) > 0:
            print u'Ссылки 1-1:'
            for toOne in self.ToOneRefs:
                print toOne.__str__()

    def _printToMany(self):
        if len(self.ToManyRefs) > 0:
            print u'Ссылки 1-ко-многим'
            for toMany in self.ToManyRefs:
                print toMany.__str__()

    def printReadable(self):
        print self.Description.__str__()

        print u'Свойства:'
        for prop in self.Properties:
            print prop.__str__()

        self._printToOneRefs()
        self._printToMany()


def getTreeRoot(filename):
    tree = ET.parse(filename)
    return tree.getroot()


def findAllByTagType(root, tagName):
    for child in root:
        if child.tag == tagName:
            yield child



        # caption = child.attrib['caption']
        # if u'лица' in caption:
        #     print caption
        #     print child.attrib['name']

def safeGet(elem, attrName):
    if attrName in elem.attrib:
        return elem.attrib[attrName]
    else:
        return ""

# script begin


class PrintDictionaries:

    dictionaries = list()

    def PrintDict(self, filename, dictionaryID):

        for child in getTreeRoot(filename):
            if child.tag == 'dictionary':
                myDict = DictionaryElement()

                desc = DictionaryDesc()
                desc.ID = safeGet(child, 'id')
                desc.Caption = safeGet(child, 'caption')
                desc.DBID = safeGet(child, 'dbid')
                desc.DBtable = safeGet(child, 'dbtable')
                desc.Name = safeGet(child, 'name')
                myDict.Description = desc
                for childElem in child:
                    if childElem.tag == 'property':
                        prop = PropertyElement()
                        prop.ID = safeGet(childElem, 'id')
                        prop.Caption = safeGet(childElem, 'caption')
                        prop.DBColumn = safeGet(childElem, 'dbcolumn')
                        prop.DisplayKey = safeGet(childElem, 'displaykey')
                        prop.Required = safeGet(childElem, 'required')
                        prop.Persistent = safeGet(childElem, 'persistent')
                        prop.Type = safeGet(childElem, 'type')

                        myDict.Properties.append(prop)

                    if childElem.tag == 'to-one-reference':
                        toOne = ToOneRefElement()
                        toOne.ID = safeGet(childElem, 'id')
                        toOne.Property = safeGet(childElem, 'property')
                        toOne.Dictionary = safeGet(childElem, 'dictionary')
                        toOne.Caption = safeGet(childElem, 'caption')

                        myDict.ToOneRefs.append(toOne)

                ddict = DictionaryElement()
                ddict.Description = myDict.Description
                ddict.ToOneRefs = list(myDict.ToOneRefs)
                ddict.ToManyRefs = list(myDict.ToManyRefs)

                self.dictionaries.append(ddict)

        self.dictionaries[dictionaryID].printReadable()


d = PrintDictionaries()
d.PrintDict('Metadata.xmd', 4)
