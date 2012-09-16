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

import os
print ('****Checking webkit lock')
if not os.path.exists('webkit.lock'): # Check lock
    LOG = Logger('Browser').get()
    file = open('webkit.lock', 'w+') # Create lock
    file.write('locking')
    file.close()
    print ('Created lock')
    
    import gi
    gi.require_version('Gtk', '3.0')
    # For .gir files sudo apt-get install libwebkitgtk-3.0-dev
    gi.require_version('WebKit', '3.0')
    
    from gi.repository import Gtk #@UnresolvedImport
    from gi.repository import WebKit #@UnresolvedImport
    from gi.repository import GObject #@UnresolvedImport
    from gi.repository import Soup #@UnresolvedImport
    
    GObject.threads_init()
    
    from base64 import b64encode
    from urllib.parse import urlparse, parse_qsl #@UnresolvedImport
    
    def _basic_auth_header(basic):
        b = '{username}:{password}'.format(**basic).encode('utf-8')
        b64 = b64encode(b).decode('utf-8')
        return {'Authorization': 'Basic ' + b64}
    
    session = WebKit.get_default_session()
    
    # clear cookies again in a new session
    try:
        os.remove('cookies.txt')
    except OSError:
        pass
    cookie_jar = Soup.CookieJarText.new('cookies.txt', False)
    session.add_feature(cookie_jar)
    
    # http://www.webkit.org/blog/1188/how-webkit-loads-a-web-page/ (pick image)
    class Browser(WebKit.WebView): #@UndefinedVariable
        __gsignals__ = {
            'render-finished': (GObject.SignalFlags.RUN_LAST,
                                None,
                                (),
                               ),
            'open': (GObject.SIGNAL_RUN_LAST, 
                     GObject.TYPE_NONE,
                     [GObject.TYPE_PYOBJECT],
                ),
            }
           
        def __init__(self):
            """
            Webkit is not thread-safe. External processing  
            on a secondary thread is OK, but any calls into the DOM will have  
            to happen on the main thread.
            http://markmail.org/message/4dwft6s6g6ptavj6
            """
            #WebKit.WebView.__init__(self)
            super().__init__()
            
            self.inspector = None
            self._env = None

            LOG.debug('WebKit ' + 
                      '.'.join([str(WebKit.MAJOR_VERSION), 
                                str(WebKit.MINOR_VERSION), 
                                str(WebKit.MICRO_VERSION),
                               ]) + 
                      ' ' +
                      '.'.join([str(WebKit.USER_AGENT_MAJOR_VERSION),
                                str(WebKit.USER_AGENT_MINOR_VERSION),
                               ])
                      )
            
            # http://webkitgtk.org/reference/webkitgtk/unstable/WebKitWebSettings.html
            self.settings = self.get_settings() # WebKit.WebSettings()

            self.settings.set_property('enable-java-applet', False)
            self.settings.set_property('enable-plugins', False)
            self.settings.set_property('enable-scripts', True)

                
            self.settings.set_property('enable-file-access-from-file-uris', True)
            self.settings.set_property('user-agent', 'FreeStation')
            self.settings.set_property('enable-private-browsing', False)
            self.settings.set_property('enable-spell-checking', False)
            self.settings.set_property('enable-universal-access-from-file-uris', True)
            self.settings.set_property('enable-dns-prefetching', True)
            self.settings.set_property('enable-webaudio', True)
            self.settings.set_property('enable-webgl', True)
            self.settings.set_property('enable-fullscreen', True)
            self.settings.set_property('enable-xss-auditor', False)
            self.settings.set_property('javascript-can-open-windows-automatically', False)
            
            self.set_size_request(-1, -1)
    
            # https://lists.webkit.org/pipermail/webkit-gtk/2010-May/000241.html
            self.connect('resource-request-starting', self._on_request)
            self.connect('resource-load-finished', self.on_resource_load_finished)
            self.connect('resource-load-failed', self.on_resource_load_failed)
            #self.connect('resource-loaded-from-memory-cache', self.on_resource_loaded_from_memory_cache)
            
            self.connect('notify::load-status', self._on_load_status)
            
            ####self.connect("title-changed", self._on_title_changed)
            ####self..connect("script-alert", self._on_script_alert)
            self.connect('notify::uri', self.on_notify_uri)
            self.connect('notify::status', self.on_notify_status)
            
            # http://webkitgtk.org/reference/webkitgtk/stable/webkitgtk-webkitwebview.html#WebKitWebView-load-error
            self.connect('notify::load-error', self.on_load_error)
            self.connect('notify::provisional-load-failed', self.on_provisional_load_failed)
            
            self.connect('load-error', self.on_load_error)
            self.connect('notify::cancel', self.on_notification_cancel)
            self.console_response = self.connect('console-message', self.on_console_message)
            
            # scale other content besides from text as well
            self.set_full_content_zoom(True)
            self.set_border_width(0)
            self.set_custom_encoding('UTF-8')
            #print self.get_custom_encoding()
            #print self.get_encoding()
    
            self.set_default_direction(Gtk.TextDirection.LTR)
            #print self.get_default_direction()
            self.set_double_buffered(True)
            self.set_transparent(True)
            self.set_editable(False)
            self.set_view_mode(False)
            self.set_view_source_mode(False)
            
            # make sure the items will be added in the end
            # hence the reason for the connect_after
            self.connect_after('populate-popup', self.populate_popup)
            self.connect('load-finished', self.on_load_finished)
            self.connect('create-web-view', self.on_create_webview)
            
            # http://webkitgtk.org/reference/webkitgtk/stable/webkitgtk-webkitwebview.html#WebKitWebView-web-view-ready
            self.connect('web-view-ready', self.on_web_view_ready)
            
            self.connect('navigation-policy-decision-requested',
                self._on_nav_policy_decision
            )
                    
            self.connect('open', self.on_open)
    
        def set_env(self, env):
            self._env = env
            if env is None:
                self._u = None
                self._oauth = None
                self._basic = None
                return
            self._u = urlparse(env['url'])
            self._oauth = env.get('oauth')
            self._basic = env.get('basic')
        
        def set_recv(self, recv):
            """ Executed by Hub object when recieve data """
            self._recv = recv
            self.connect('notify::title', self._on_notify_title)
        
        def _on_notify_title(self, view, notify):
            title = view.get_property('title')
            print ('Title (on notify title): ' + str(title))
            if title is None:
                return
            self._recv(title)
        
        def on_open(self, view, uri):
            import subprocess
            subprocess.check_call(['/usr/bin/xdg-open', uri])
        
        def on_console_message(self, *args):
            """ callback on 'console-message' webkit.WebView signal """
            
            (view, message, line, file) = args
            print ('browser: ' + str(message) + ' in file: ' + str(file) + ' line:' + str(line))
            self.stop_emission('console-message')
        
        def on_web_view_ready(self, view):
            print ('WEBVIEW READY')
        
        def _on_nav_policy_decision(self, view, frame, request, nav, policy):
            """
            Handle user trying to Navigate away from current page.
    
            Note that this will be called before `CouchView._on_resource_request()`.
    
            The *policy* arg is a ``WebPolicyDecision`` instance.  To handle the
            decision, call one of:
    
                * ``WebPolicyDecision.ignore()``
                * ``WebPolicyDecision.use()``
                * ``WebPolicyDecision.download()``
    
            And then return ``True``.
    
            Otherwise, return ``False`` or ``None`` to have the WebKit default
            behavior apply.
            """
            pass
        
            """
            if self._env is None:
                print ('ENVIROMENT NONE _on_nav_policy_decision')
                return
            uri = request.get_uri()
            u = urlparse(uri)
            print ('URI NETLOC:' + str(u.netloc))
            if u.netloc == self._u.netloc or u.scheme == 'file':
                return False
            if u.scheme in ('http', 'https'):
                self.emit('open', uri)
            policy.ignore()
            return True"""
        
        def on_notification_cancel(self):
            print ('CANCELL')
            
        def on_resource_loaded_from_memory_cache(self, web_view, web_frame, uri, web_error):
            print ('on_resource_loaded_from_memory_cache', web_view, web_frame, uri, web_error)
        
        # loaded-from-memory-cache
        # resource-will-be-cached
        # will-be-cached
        def on_provisional_load_failed(self, web_view, web_frame, uri, web_error):
            print ('PROVISIONAL LOAD FAILED', web_view, web_frame, uri, web_error)
            
        def on_load_error(self, web_view, web_frame, uri, web_error):
            print ('LOAD ERROR', web_view, web_frame, uri, web_error)
            
            response = web_frame.get_network_response() # WebKitNetworkResponse
            uri = response.get_uri()
            message = response.get_message()
            
            print ('Response uri:' + str(uri))
            print ('Response message:' + str(message))
        
            if message:
                print ('message method:' + str(message.props.method))  
                print ('message uri:' + str(message.props.uri))
                print ('message http_version:' + str(message.props.http_version))
                print ('message flags:' + str(message.props.flags))
                print ('message server_side:' + str(message.props.server_side))
                print ('message status_code:' + str(message.props.status_code))
                print ('message reason_phrase:' + str(message.props.reason_phrase))
                print ('message first_party:' + str(message.props.first_party))
                print ('message request_body:' + str(message.props.request_body))
                print ('message request_headers:' + str(message.props.request_headers))
                print ('message tls_certificate:' + str(message.props.tls_certificate))
                print ('message tls_errors:' + str(message.props.tls_errors))
                
            import traceback
            #print traceback.print_tb()
            
            try:
                splash = open('templates/splash.html', 'r').read() # Eclipse path
            except IOError:
                import os
                file_path = str(os.path.split(os.path.dirname(__file__))[0])
                splash = open(file_path + '/templates/splash.html', 'r').read()
            
            if not uri:
                response.set_uri('uclm_demo.html')
            self.reload_bypass_cache()
            
        def on_create_webview(self, browser, web_frame):
            print ('=> on create webview ', browser, web_frame)
            
        def on_load_finished(self, browser, web_frame):
            print ('=> event load finished ') #, browser, web_frame
    
            print ('Provisonal data source:', web_frame.get_provisional_data_source())
            print ('Title:', web_frame.get_title())
            print ('URI:', web_frame.get_uri())
        
        def on_notify_status(self, browser, uri): # download status
            print ('Notify status')
            
        def on_notify_uri(self, browser, uri):
            print ('Notify uri')
            
        def _on_load_status(self, view, browser):
            if view.get_property('load-status') == WebKit.LoadStatus.FINISHED:
                print ('* Browser load finished')
                # this needs to run with a timeout because otherwise the
                # status is emited before the offscreen image is finihsed
                GObject.timeout_add(100, lambda: self.emit("render-finished"))
            elif view.get_property('load-status') == WebKit.LoadStatus.FAILED:
                print ('* Browser load failed')
                
            elif view.get_property('load-status') == WebKit.LoadStatus.COMMITTED:
                print ('* Browser load commited')
            elif view.get_property('load-status') == WebKit.LoadStatus.PROVISIONAL:
                print ('* Browser load provisional')
            elif view.get_property('load-status') == WebKit.LoadStatus.FIRST_VISUALLY_NON_EMPTY_LAYOUT:
                print ('* Browser load provisional')
                
        def populate_popup(self, view, menu):
            # zoom buttons
            zoom_in = Gtk.ImageMenuItem(Gtk.STOCK_ZOOM_IN)
            #zoom_in.connect('activate', zoom_in_cb, view)
            menu.append(zoom_in)
      
            zoom_out = Gtk.ImageMenuItem(Gtk.STOCK_ZOOM_OUT)
            #zoom_out.connect('activate', zoom_out_cb, view)
            menu.append(zoom_out)
      
            zoom_hundred = Gtk.ImageMenuItem(Gtk.STOCK_ZOOM_100)
            #zoom_hundred.connect('activate', zoom_hundred_cb, view)
            menu.append(zoom_hundred)
      
            printitem = Gtk.ImageMenuItem(Gtk.STOCK_PRINT)
            menu.append(printitem)
            #printitem.connect('activate', print_cb, view)
      
            page_properties = Gtk.ImageMenuItem(Gtk.STOCK_PROPERTIES)
            menu.append(page_properties)
            # page_properties.connect('activate', page_properties_cb, view)
      
            menu.append(Gtk.SeparatorMenuItem())
      
            aboutitem = Gtk.ImageMenuItem(Gtk.STOCK_ABOUT)
            menu.append(aboutitem)
            #aboutitem.connect('activate', about_pywebkitgtk_cb, view)
      
            menu.show_all()
            return False
        
        def _on_request(self, view, frame, resource, request, response):
            print ('  on request', view, frame, resource, request, response)
            
            if request:
                message = request.get_message() # SoupMessage
            
            if resource:
                uri = request.get_uri()
                
                print ('  Resource data:')
                print ('    Data:', resource.get_data())
                print ('    URI:', uri)
                print ('    MIME:', resource.get_mime_type())
                print ('    Frame:', resource.get_frame_name())
            #print uri
            
            if self._env is None:
                print ('ENVIROMENT NONE ON REQUEST')
                return
            uri = request.get_uri()
            message = request.get_message() # SoupMessage
            print ('URI:' + str(uri))
    
            u = urlparse(uri)
            if u.netloc != self._u.netloc:
                print ('netloc:' + str(u.netloc))
                print ('self netloc:' + str(self._u.netloc))
                return
            if u.scheme != self._u.scheme:
                print ('scheme:' + str(u.scheme))
                print ('self scheme:' + str(self._u.scheme))
                return
            if self._oauth:
                print ('oauth CALL FIRST TIME')
                """query = dict(parse_qsl(u.query))
                if u.query and not query:
                    query = {u.query: ''}
                baseurl = ''.join([u.scheme, '://', u.netloc, u.path])
                print ('baseurl:' + str(baseurl))
                method = message.method
                print ('method:' + str(method))
                h = _oauth_header(self._oauth, method, baseurl, query)"""
            elif self._basic:
                # http://comments.gmane.org/gmane.os.opendarwin.webkit.gtk/1194
                # http://webkitgtk.org/reference/webkitgtk/stable/WebKitSoupAuthDialog.html
                print (WebKit.get_default_session().new())
                h = _basic_auth_header(self._basic)
            else:
                return

            print ('request message method:' + str(request.props.message.props.method))  
            print ('request message uri:' + str(request.props.message.props.uri))
            print ('request message http_version:' + str(request.props.message.props.http_version))
            print ('request message flags:' + str(request.props.message.props.flags))
            print ('request message server_side:' + str(request.props.message.props.server_side))
            print ('request message status_code:' + str(request.props.message.props.status_code))
            print ('request message reason_phrase:' + str(request.props.message.props.reason_phrase))
            print ('request message first_party:' + str(request.props.message.props.first_party))
            print ('request message request_body:' + str(request.props.message.props.request_body))
            print ('request message request_headers:' + str(request.props.message.props.request_headers))
            print ('request message tls_certificate:' + str(request.props.message.props.tls_certificate))
            print ('request message tls_errors:' + str(request.props.message.props.tls_errors))
            
            # http://developer.gnome.org/libsoup/stable/SoupSession.html#SoupSession-authenticate

            # Removes all the headers listed in the Connection header.
            message.request_headers.clean_connection_headers()
            
            print ('request uri:' + str(request.props.uri))
                
            for (key, value) in h.items():
                print ('key:' + str(key))
                print ('value:' + str(value))
                message.request_headers.append(key, value)
    
            print('COOKIES' + str(Soup.cookies_from_request(message)))
            
            print('AUTH' + str(message.request_headers.get("Authorization")))
            print('Referer' + str(message.request_headers.get("Referer")))
            print('Connection' + str(message.request_headers.get("Connection")))
            print('Content-Type' + str(message.request_headers.get("Content-Type")))
            print('Timeout' + str(message.request_headers.get("Timeout")))
            print('Accept' + str(message.request_headers.get("Accept")))
    
            # http://developer.gnome.org/libsoup/stable/SoupMessage.html
            print ('STATUS HTTP STATUS' + str(request.props.message.get_https_status()))
            print ('STATUS HTTP VERSION' + str(request.props.message.get_http_version()))
            print ('STATUS HTTP URI' + str(request.props.message.get_uri()))
            print ('STATUS HTTP ADDRESS' + str(request.props.message.get_address()))
            print ('STATUS HTTP FLAGS' + str(request.props.message.get_flags()))
            print ('STATUS KEEPALIVE' + str(request.props.message.is_keepalive()))
            print ('STATUS get_first_party' + str(request.props.message.get_first_party()))

                
            print ('STATUS get_' + str(request.props.message.props.request_headers.get_list(str(Soup.MessageHeadersType.RESPONSE))))

            """SoupMessageHeaders
            SOUP_MESSAGE_HEADERS_REQUEST
            request headers
            SOUP_MESSAGE_HEADERS_RESPONSE
            Soup.MessageHeadersType.REQUEST
            SoupHTTPVersion.SOUP_HTTP_1_1"""
    
        def on_resource_load_failed(self, view, frame, resource = None, reason = None): # , resource
            print ('  on resource load failed', view, frame, resource, reason)#, resource
            
            if resource:
                print (resource.get_data())
                print (resource.get_uri())
                print (resource.get_mime_type())
                print (resource.get_frame_name())
               
        def on_resource_load_finished(self, view, frame, resource):
            print ('on resource load finished', view, frame, resource)
            if resource:
                print (resource.get_data())
                print (resource.get_uri())
                print (resource.get_mime_type())
                print (resource.get_frame_name())
        
        def _on_reload(self):
            self.reload_bypass_cache()
            print ('reloading on_reload')
            
            """ 
            u = urlparse(uri)
            if u.netloc != self._u.netloc:
                return
    
            if u.scheme != self._u.scheme:
                return
    
            if self._oauth:
                query = dict(parse_qsl(u.query))
                
                if u.query and not query:
                    query = {u.query: ''}
                    
                baseurl = ''.join([u.scheme, '://', u.netloc, u.path])
                method = request.props.message.props.method
                h = _oauth_header(self._oauth, method, baseurl, query)
            elif self._basic:
                h = _basic_auth_header(self._basic)
            else:
                return
    
            for (key, value) in h.items():
                request.props.message.props.request_headers.append(key, value)
            """
         
            """
         def about_pywebkitgtk_cb(menu_item, web_view):
        web_view.open("http://live.gnome.org/PyWebKitGtk")
      
    def zoom_in_cb(menu_item, web_view):
        ""Zoom into the page""
        web_view.zoom_in()
      
    def zoom_out_cb(menu_item, web_view):
        ""Zoom out of the page""
        web_view.zoom_out()
      
    def zoom_hundred_cb(menu_item, web_view):
        ""Zoom 100%""
        if not (web_view.get_zoom_level() == 1.0):
            web_view.set_zoom_level(1.0)
      
    def print_cb(menu_item, web_view):
        mainframe = web_view.get_main_frame()
        mainframe.print_full(gtk.PrintOperation(), gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG);
      
    def page_properties_cb(menu_item, web_view):
        mainframe = web_view.get_main_frame()
        datasource = mainframe.get_data_source()
        main_resource = datasource.get_main_resource()
        window = gtk.Window()
        window.set_default_size(100, 60)
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("MIME Type :"), False, False)
        hbox.pack_end(gtk.Label(main_resource.get_mime_type()), False, False)
        vbox.pack_start(hbox, False, False)
        hbox2 = gtk.HBox()
        hbox2.pack_start(gtk.Label("URI : "), False, False)
        hbox2.pack_end(gtk.Label(main_resource.get_uri()), False, False)
        vbox.pack_start(hbox2, False, False)
        hbox3 = gtk.HBox()
        hbox3.pack_start(gtk.Label("Encoding : "), False, False)
        hbox3.pack_end(gtk.Label(main_resource.get_encoding()), False, False)
        vbox.pack_start(hbox3, False, False)
        window.add(vbox)
        window.show_all()
        window.present()
            """
