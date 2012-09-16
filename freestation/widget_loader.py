#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# This file is part of FreeStation.
#
# FreeStation is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# FreeStation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fail2Ban; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Author: Ángel Guzmán Maeso
# 
# $Revision$

__author__    = 'Ángel Guzmán Maeso'
__version__   = '$Revision$'
__date__      = '$Date$'
__copyright__ = 'Copyright (c) 2012 Ángel Guzmán Maeso'
__license__   = 'GPL'

from logger import Logger
LOG = Logger('WidgetLoader').get()

from os.path import join
from xml.dom.minidom import parse

from base_exception import FSBaseException

class WidgetXMLFileNotFound(FSBaseException):
    def __doc__(self): #@ReservedAssignment
        '''
            Throwed when widget.xml is not found.
        '''
        pass

class WidgetXMLBadFormed(FSBaseException):
    def __doc__(self): #@ReservedAssignment
        '''
            Throwed when widget.xml is bad formed.
        '''
        pass

class WidgetLoader(object):
    
    __gtype_name__ = 'WidgetLoader'
    __name__       = 'WidgetLoader'

    def __init__(self):
        self._load_xml()
        self._read_data()
        
    def _load_xml(self):
        try:
            self.widget_source = open(join('xml', 'widgets.xml'))
            LOG.debug('widgets.xml loaded')
        except Exception as e:
            LOG.exception('WidgetXMLFileNotFound: {0}'.format(e))
            raise WidgetXMLFileNotFound('Could not load the widgets.xml file')
        
        self.dom = parse(self.widget_source)
       
    def get_document_element(self):
        '''
            Check and try to get the document element "widgets"
            Try with self.dom.firstChild if not found
        '''
        if self.dom.documentElement.nodeType == self.dom.documentElement.ELEMENT_NODE:
            if self.dom.documentElement.nodeName == 'interface':
                return self.dom.documentElement
            else:
                raise WidgetXMLBadFormed('Document element is not a interface element node.')
        else:
            raise WidgetXMLBadFormed('Document element is not a element node.')
        
    def _read_data(self):
        '''
            Read all the content with checking for widgets.xml
        '''
        LOG.debug('Document Version {0}'.format(self.dom.version))
        
        self.document = self.get_document_element()
        self._read_child_nodes()

    def _filter_element_nodes(self, main_node, node_name):
        '''
            Read and filter the document element node and
            return a list of widgets that are only element nodes
        '''
        nodes = []
        for node in main_node.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node_name == None:
                    nodes.append(node)
                elif node.nodeName == node_name:
                    nodes.append(node)
                
        return nodes
        
    def _read_child_nodes(self):   
        '''
            Read all the child nodes contained by the document element
            on widgets.xml
 
            NodeTypes:
               ELEMENT_NODE                = 1
               ATTRIBUTE_NODE              = 2
               TEXT_NODE                   = 3
               CDATA_SECTION_NODE          = 4
               ENTITY_REFERENCE_NODE       = 5
               ENTITY_NODE                 = 6
               PROCESSING_INSTRUCTION_NODE = 7
               COMMENT_NODE                = 8
               DOCUMENT_NODE               = 9
               DOCUMENT_TYPE_NODE          = 10
               DOCUMENT_FRAGMENT_NODE      = 11
               NOTATION_NODE               = 12
        '''
        
        self.widgets = self.document.getElementsByTagName('widget')
        self.result = []

        for widget in self.widgets:
            widget_name = widget.getElementsByTagName('name')[0].childNodes[0].nodeValue
            
            properties_node = widget.getElementsByTagName('properties')
            for properties_node_item in properties_node:
                properties = self._filter_element_nodes(properties_node_item, None)
            
                propertie_result = []
                for propertie in properties:
                    propertie_name = propertie.nodeName
                    propertie_value = None
                    if propertie.childNodes:
                        propertie_value = propertie.childNodes[0].nodeValue
                    propertie_result.append((propertie_name, propertie_value))
                    
            self.result.append((widget_name, propertie_result))
            
    def get_widgets(self):
        return self.result
                             
if __name__ == '__main__':
    WidgetLoader()