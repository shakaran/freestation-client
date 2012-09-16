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

from freestation.logger import Logger
LOG = Logger('UclmDemo').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from gi.repository import GdkPixbuf #@UnresolvedImport

import os
from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

from freestation.widgets.ButtonSection import ButtonSection
from freestation.widgets.NewsInfo import NewsInfo
from freestation.widgets.ScrolledBox import ScrolledBox
from freestation.widgets.WhiteLabel import WhiteLabel
from freestation.widgets.MountInfo import MountInfo
from freestation.widgets.ScrollableText import ScrollableText

class UclmDemo(Gtk.Box):
    __gtype_name__ = 'UclmDemo'
    __name__ = 'UclmDemo' #@ReservedAssignment
    
    DEFAULT_BACKGROUND   = '#660707'
    DEFAULT_BORDER_WIDTH = 24
    
    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        LOG.debug('Starting')
        
        self.current_section = None
        self.sections = []
        self.display_box = Gtk.VBox()        
        self.listing_box = Gtk.VBox()
      
    def icon_load(self, icon_name):
        icon = os.path.split(os.path.dirname(__file__))[0] + "/img/" + icon_name
        return icon
    
    def create_status_box(self):
        self.status_box = Gtk.HBox()
        self.status_box.pack_start(self.home_button, expand = False, fill = False, padding = 0)
    
    def create_home_button(self):
        self.home_icon = self.icon_load('home-button.png')
        
        self.home_button = ButtonSection('Inicio', self.home_icon, 'pink')
        self.home_button.button.connect('clicked', self.on_button_home)
    
    def create_distribution_button(self):
        self.distributions_icon = self.icon_load('distributions-button.png')
        self.distributions_button = ButtonSection('Descargar ISO de distribuciones GNU/Linux', self.distributions_icon, 'pink')
        self.sections.append(self.distributions_button)
    
    def create_software_button(self):     
        self.software_icon = self.icon_load('software-button.png')
        self.software_button = ButtonSection('Descarga software libre para Windows', self.software_icon, 'pink')
        self.sections.append(self.software_button)

    def create_documentation_button(self):     
        self.documentation_icon = self.icon_load('documentation-button.png')
        self.documentation_button = ButtonSection('Manuales de software', self.documentation_icon, 'pink')
        self.sections.append(self.documentation_button)        
        
    def create_resources_button(self):    
        self.resources_icon = self.icon_load('resources-button.png')
        self.resources_button = ButtonSection('Apuntes de asignaturas', self.resources_icon, 'pink')
        self.sections.append(self.resources_button)
        
    def create_news_info_widget(self):
        self.news_info_widget = NewsInfo(None)
        self.news_info_widget.start()
        
    def main_page(self):
        
        self.create_home_button()
        
        self.create_status_box()
        
        self.create_distribution_button()
        self.create_software_button()
        self.create_documentation_button()
        self.create_resources_button()

        self.distributions_button.button.connect('clicked', self.on_distributions_button_click, self.distributions_button, self.sections)

        self.display_box.pack_start(self.distributions_button, True, True, True)
        self.display_box.pack_start(self.software_button, True, True, True)
        self.display_box.pack_start(self.documentation_button, True, True, True)
        self.display_box.pack_start(self.resources_button, True, True, True)
        
        self.listing_box.pack_start(self.status_box, expand = False, fill = False, padding = 0)
        self.listing_box.pack_start(self.display_box, True, True, True)

        self.create_news_info_widget()

        self.pack_start(self.listing_box, expand = True, fill = True, padding = 0)
        self.pack_start(self.news_info_widget, expand = False, fill = False, padding = 0)
        self.show_all()

    def on_distro_button(self, widget, data):
        print ('on distro', widget, data)
        
        distro = { 'molinux' : """
        MOLINUX
        
        MoLinux es la distribución GNU/Linux oficial de la Junta de 
        Comunidades de Castilla-La Mancha. MoLinux está basado en Ubuntu. 
        
        Los nombres de cada versión son personajes de la novela 
        "El ingenioso hidalgo don Quijote de la Mancha", de Miguel de 
        Cervantes.
        
        MoLinux es una iniciativa comenzada en 2005 de la JCCM para 
        introducir a la comunidad castellano-manchega en la vanguardia 
        de la Sociedad de la Información. El proyecto MoLinux ataca la 
        brecha digital reduciendo los costes del software y ofreciendo 
        un sistema operativo fácil de usar. MoLinux es un sistema operativo 
        general. Pronto estarán disponibles versiones modulares adaptadas 
        a usos más específicos.
        
        El compromiso con la filosofía 'software libre' es tal que el 
        gobierno castellano manchego no impondrá en ningún caso el uso 
        de 'Molinux'. "La ventaja es que el 'software' libre no tiene que 
        competir con nadie, y el usuario puede elegir entre usar este u otro 
        tipo de 'software'".
        """,
        'debian' : """
        DEBIAN
        
        Debian es un sistema operativo gratuito, una de las distribuciones de 
        Linux más populares e influyentes.

        Debian es conocido por su adhesión a las filosofías del software 
        libre y por su abundancia de opciones (su actual versión incluye 
        más de 18 mil paquetes de software, para once arquitecturas de 
        computadora).

        Debian GNU/Linux, también es base para otras múltiples 
        distribuciones de Linux como Knoppix, Linspire, MEPIS, Xandros y la 
        familia Ubuntu.

        Debian también es conocido por su sistema de gestión de paquetes 
        (especialmente APT), por sus estrictas políticas con respecto a sus 
        paquetes y la calidad de sus lanzamientos. Estas prácticas permiten 
        fáciles actualizaciones entre lanzamientos, y una instalación y 
        removión sencilla de paquetes.

        También utiliza un desarrollo y proceso de testeo abiertos. Es 
        desarrollado por voluntarios de todo el mundo, y apoyado por 
        donaciones a través de la "Software in the Public Interest", 
        una organización sin fines de lucro para el apoyo de proyectos 
        de software libre.
        """,
        'ubuntu' : """
        UBUNTU
        
        Ubuntu GNU/Linux es un sistema operativo basado en el núcleo Linux y 
        en algunas herramientas del Proyecto GNU. 
        
        La estructura técnica del 
        sistema está basada en el Proyecto Debian, pero el planteamiento 
        está inspirado en los principios de la corriente ubuntu, un 
        movimiento humanista encabezado por el obispo Desmond Tutu, 
        Premio Nobel de la Paz 1984. 
        
        Económicamente el proyecto se 
        sostiene con aportaciones de la empresa Canonical del millonario 
        sudafricano Mark Shuttleworth. 
        """,
        'arch' : """
        ARCH
        
        Arch Linux es una distribución desarrollada por la comunidad en forma 
        independiente y optimizada para i686/x86-64, basada en un modo de 
        liberado continuo y dirigida a usuarios con un nivel intermedio y 
        avanzado. Ofrece un gran repositorio con binarios y un excelente 
        gestor de paquetes, así como un sistema de paquetes parecido a los 
        ports. El desarrollo se centra sobre un balance de minimalismo, 
        elegancia, correcciones de código y modernidad.
        
        Está basadá originalmente en las ideas de CRUX, una gran 
        distribución desarrollada por Per Lidén. La versión 0.1 
        (Homero) de Arch Linux fue lanzada el 11 de marzo de 2002.

        Arch provee un entorno mínimo después de la instalación (sin GUI), 
        compilado para arquitecturas i686/x86-64. Arch es ligera, flexible, 
        rápida, simple y apunta a ser muy similar a UNIX. Su diseño, 
        filosofía e implementación hace fácil extenderla y moldearla a 
        cualquier tipo de sistema que estés construyendo: desde una 
        máquina de consola minimalista al más grandioso entorno de 
        escritorio habilitado con ricas características. 
        
        En lugar de arrancar paquetes innecesarios y no deseados Arch ofrece, 
        al usuario, el poder y la capacidad para construir desde una base 
        mínima sin ninguna opción por defecto. El usuario es quién decide 
        que Arch Linux instalará.
        """,
        'gentoo' : """
        GENTOO
        
        Gentoo Linux es una distribución GNU/Linux orientada a usuarios con 
        cierta experiencia en este sistema operativo, fue fundada por 
        Daniel Robbins, basada en la inactiva distribución llamada Enoch 
        Linux. 
        
        Ya para el año 2002, ésta última pasa a denominarse Gentoo Linux.

        El nombre Gentoo proviene del nombre en inglés del pingüino papúa. 
        Nótese que la mascota de Linux es un pingüino.

        La piedra angular de Gentoo es Portage, un sistema de distribución 
        de software basado en Ports de BSD. Portage consiste en un árbol 
        local, que contiene las descripciones de los paquetes de software, 
        así como los scripts necesarios para instalarlos. 
        
        Este árbol se puede sincronizar con un servidor remoto mediante una orden.
        """,
        'centos' : """
        CENTOS
        
        CentOS (acrónimo de Community ENTerprise Operating System) es un 
        clon a nivel binario de la distribución Red Hat Enterprise Linux, 
        compilado por voluntarios a partir del código fuente liberado por 
        Red Hat, empresa desarrolladora de RHEL.

        Red Hat Enterprise Linux se compone de software libre y código 
        abierto, pero se publica en formato binario usable (CD-ROM o DVD-ROM) 
        solamente a suscriptores pagados. 
        
        Como es requerido, Red Hat libera 
        todo el código fuente del producto de forma pública bajo los términos 
        de la Licencia Pública GNU y otras licencias. Los desarrolladores de 
        CentOS usan ese código fuente para crear un producto final que es 
        muy similar al Red Hat Enterprise Linux y está libremente disponible 
        para ser bajado y usado por el público, pero no es mantenido ni 
        soportado por Red Hat. 
        
        Existen otras distribuciones también 
        derivadas de los fuentes de Red Hat.

        CentOS usa yum para bajar e instalar las actualizaciones, 
        herramienta también utilizada por Fedora Core.
        """,}
        self.description_content.label.set_text(distro[data])

    def on_distributions_button_click(self, other, widget, sections):
        print ('On click', other, widget, sections)
        if not self.current_section or self.current_section != widget:
            self.current_section = widget
            
            self.news_info_widget.destroy()
            if hasattr(self, 'right_side_box'):
                self.right_side_box.destroy()
            
            self.description_title = WhiteLabel('Descripción')
            self.description_content = ScrollableText("""
            Una distribución de Gnu/Linux es una distribución de software 
            basada en el núcleo Linux que incluye determinados paquetes de 
            software para satisfacer las necesidades de un grupo específico 
            de usuarios, dando así origen a ediciones domésticas, 
            empresariales y para servidores. 
            
            En general, las distribuciones Linux pueden ser:
                * Comerciales o no comerciales.
                * Ser completamente libres o incluir software privativo.
                * Diseñadas para uso en el hogar o en las empresas.
                * Diseñadas para servidores, escritorios o dispositivos empotrados.
                * Orientadas a usuarios regulares o usuarios avanzados.
            
            Es un sistema operativo muy completo, con un escritorio sencillo y cómodo. 
            Lleva "de serie" el software necesario para las tareas más habituales: 
                * Conectarse a Internet
                * Mensajería instantánea
                * Navegación web
                * Gestor de correo electrónico
                 
            Además, también dispone de todas las funciones de edición de 
            textos, hojas de cálculo, 
            bases de datos, edición de imágenes, etc.
            
            En la actualidad existen gran cantidad de distribuciones, 
            cada una de ellas creada para satisfacer unas necesidades 
            concretas y con un objetivo específico, como es la facilidad 
            de uso, la seguridad, su utilización por un colectivo determinado, 
            etc, 
            
            Las distribuciones GNU/Linux vienen completamente pre-configuradas 
            según las especificaciones establecidas por la organización que 
            las crea, incluyendo utilidades e instaladores.
            
            La mayoría de las distribuciones están, en mayor o menor medida, 
            desarrolladas y dirigidas por sus comunidades de desarrolladores y 
            usuarios. En algunos casos están dirigidas y financiadas 
            completamente por la comunidad. como ocurre con Debian GNU/Linux, 
            mientras que otras mantienen una distribución comercial y una 
            versión de la comunidad.
            
            """)
            
            self.description_box = Gtk.VBox()
            self.description_box.pack_start(self.description_title, expand = False, fill = False, padding = 0)
            self.description_box.pack_start(self.description_content, expand = True, fill = True, padding = 0)
            
            self.description_box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#D35F5F"))
            
            boxie = Gtk.EventBox()
            boxie.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#D35F5F")) 
                
            self.description_box.add(boxie)
            
            copy_usb_icon = self.icon_load('copy-usb-button.png')
            copy_usb_button = ButtonSection('Copiar al USB', copy_usb_icon, 'pink', True)
            
            
            self.mount_info = MountInfo(None)
            
            self.mount_info_box = Gtk.HBox()
            self.mount_info_box.pack_start(Gtk.HBox(), expand = True, fill = True, padding = 0)
            self.mount_info_box.pack_start( self.mount_info, expand = False, fill = False, padding = 0)
            self.mount_info_box.pack_start(Gtk.HBox(), expand = True, fill = True, padding = 0)
            
            usb_bootable_icon = self.icon_load('usb-bootable-button.png')
            usb_bootable_button = ButtonSection('USB Bootable', usb_bootable_icon, 'pink', True)
            
            self.action_label = WhiteLabel('Actions')
            self.action_label.set_margin_top(15)
            self.action_label.set_margin_bottom(15)
            
            self.actions_box     = Gtk.VBox()
            self.actions_box.pack_start(self.action_label, expand = False, fill = False, padding = 0)
            self.actions_box.pack_start(copy_usb_button, expand = False, fill = False, padding = 0)
            self.actions_box.pack_start(usb_bootable_button, expand = False, fill = False, padding = 0)
            self.actions_box.pack_start(Gtk.HBox(), expand = False, fill = False, padding = 0)
            
            self.right_side_box = Gtk.VBox()
            self.right_side_box.pack_start(self.description_box, expand = True, fill = True, padding = 0)
            self.right_side_box.pack_start(self.mount_info_box, expand = False, fill = False, padding = 0)
            self.right_side_box.pack_start(self.actions_box, expand = False, fill = False, padding = 0)
            self.right_side_box.show_all()
            
            self.pack_start(self.right_side_box, expand = True, fill = True, padding = 25)
            #self.show_all()

            molinux_icon = self.icon_load('molinux-button.png')
            debian_icon = self.icon_load('debian-button.png')
            ubuntu_icon = self.icon_load('ubuntu-button.png')
            arch_icon = self.icon_load('arch-button.png')
            gentoo_icon = self.icon_load('gentoo-button.png')
            centos_icon = self.icon_load('centos-button.png')
            
            self.molinux_button = ButtonSection('Fecha: 10-07-2012 Version: 7.0', molinux_icon, 'pink', True)
            self.debian_button = ButtonSection('Fecha: 18-07-2012 Version: 6.0', debian_icon, 'pink', True)
            self.ubuntu_button = ButtonSection('Fecha: 29-04-2012 Version: 12.04', ubuntu_icon, 'pink', True)
            self.arch_button = ButtonSection('Fecha: 03-02-2011 Version: 2.0', arch_icon, 'pink', True)
            self.gentoo_button = ButtonSection('Fecha: 20-10-2012 Version: 4.0', gentoo_icon, 'pink', True)
            self.centos_button = ButtonSection('Fecha: 04-04-2012 Version: 6.3', centos_icon, 'pink', True)
            
            """
            distros = ['molinux', 'debian', 'ubuntu', 'arch', 'gentoo', 'centos']
            for distro in distros:
                eval('self.' + str(distro) + '_button.button.connect("clicked", self.on_distro_button, "' + distro + '")' , {'__import__': None}, {})
            
            """   
            self.molinux_button.button.connect('clicked', self.on_distro_button, 'molinux')
            self.debian_button.button.connect('clicked', self.on_distro_button, 'debian')
            self.ubuntu_button.button.connect('clicked', self.on_distro_button, 'ubuntu')
            self.arch_button.button.connect('clicked', self.on_distro_button, 'arch')
            self.gentoo_button.button.connect('clicked', self.on_distro_button, 'gentoo')
            self.centos_button.button.connect('clicked', self.on_distro_button, 'centos')
        
            
            items_box = ScrolledBox() #ScrolledBox()
            items_box.pack_start(self.molinux_button, expand = True, fill = True, padding = 0)
            items_box.pack_start(self.debian_button, expand = True, fill = True, padding = 0)
            items_box.pack_start(self.ubuntu_button, expand = True, fill = True, padding = 0)
            items_box.pack_start(self.arch_button, expand = True, fill = True, padding = 0)
            items_box.pack_start(self.gentoo_button, expand = True, fill = True, padding = 0)
            items_box.pack_start(self.centos_button, expand = True, fill = True, padding = 0)

            items_box.show()
            
            view = Gtk.ScrolledWindow()
            view.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
            view.add_with_viewport(items_box) 
            view.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
            view.set_size_request(800, 800)
            view.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
            #view.set_policy(Gtk.POLICY_NEVER, Gtk.POLICY_NEVER)
            #view.set_shadow_type(Gtk.SHADOW_NONE)
            
            self.display_box.pack_end(view, expand = False, fill = False, padding = 0)
            self.display_box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
            
            boxie = Gtk.EventBox()
            boxie.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("red")) 
                
            self.display_box.add(boxie)
                
            self.display_box.show_all()
            
            for section in sections:
                if section != widget:
                    section.hide()
            
            print (self.listing_box.get_children()[1].get_children()[5].get_children()[0])
            
            viewport = self.listing_box.get_children()[1].get_children()[5].get_children()[0]
            viewport.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#AA0000'))
    
    def on_button_home(self, widget):
        if self.listing_box:
            self.listing_box.destroy()
        
        if self.right_side_box:
            self.right_side_box.destroy()
        
        if self.news_info_widget:
            self.news_info_widget.destroy()
            
        self.main_page()
        
        #.get_children()
        #self.main_page()
        
        