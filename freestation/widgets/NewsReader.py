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

# sudo apt-get install python-feedparser
# http://code.google.com/p/feedparser/
# http://pypi.python.org/pypi/feedparser/
# http://packages.python.org/feedparser/index.html
# http://kurtmckee.livejournal.com/tag/feedparser    

from freestation.logger import Logger
LOG = Logger('FeedReader').get()

import feedparser

class NewsReader:
    
    from freestation import __version__ as VERSION
    
    USER_AGENT  = 'FreeStation/' + str(VERSION) + ' +http://yourdomain.com/'
    MAX_ENTRIES = 5
    
    def __init__(self, data):
        
        LOG.debug('FeedParser v{0}'.format(str(feedparser.__version__)))
        feedparser.RESOLVE_RELATIVE_URIS = 1
        feedparser.USER_AGENT = self.USER_AGENT
        
        self.url_feed = data
        
        self.content = feedparser.parse(
                                            self.url_feed, 
                                            agent = self.USER_AGENT, 
                                            referrer = 'http://yourdomain.com/',
                                            #extra_headers={'Cache-control': 'max-age=0'},
                                        )
        
    def render(self):
        
        feed = self.content.feed
        """
        if hasattr(feed, 'version'):
            print 'Feed version:', feed.version
        
        if hasattr(feed, 'headers'):
            print 'Headers:', feed.headers
        
        if hasattr(feed, 'etag'):
            print 'Etag:', feed.etag
        
        if hasattr(feed, 'status'):
            print 'Status:', feed.status
        
        if hasattr(feed, 'modified'):
            print 'Modified:', feed.modified
        """
        
        #if hasattr(feed, 'image'):
        #    print 'Image:', feed.image
        #    print 'Image(title):', feed.image.title
        #    print 'Image(href):', feed.image.href
        #    print 'Image(width):', feed.image.width
        #    print 'Image(height):', feed.image.height
        #    print 'Image(link):', feed.image.link
            
        #if feed.has_key('ttl'):
        #    print 'TTL:', feed.get('ttl', 60)
        
        if feed.has_key('title'):
            self.title = feed.get('title', 'No title')
            #print 'Title:', self.title # feed.title
        else:
            self.title = 'No title'
            
        # http://packages.python.org/feedparser/namespace-handling.html
        #print 'Description:', feed.description
        #print 'Link:', feed.link
        
        #if feed.has_key('info'):
        #    print 'Info:', feed.info
            
        #if feed.has_key('rights'):
        #    print 'Rights:', feed.rights
        
        #print 'Published:',
        #if hasattr(feed, 'published'):
        #    print feed.get('published', 'No published date') # feed.published
        #else:
        #    print 'No published date'
            
        #if hasattr(feed, 'published_parsed'):
        #    print 'Published(parsed):', feed.published_parsed
        
        #print 'Subtitle:', feed.subtitle
        #print 'Subtitle(detail):', feed.subtitle_detail
        #if hasattr(feed, 'updated'):
        #    print feed.updated

        #if hasattr(feed, 'categories'):
        #    print 'Categories:', feed.categories
           
        #if hasattr(feed, 'cloud'):
           # print 'Cloud:', feed.cloud
            #print 'Cloud(domain):', feed.cloud.domain
            #print 'Cloud(port):', feed.cloud.port
            #print 'Cloud(path):', feed.cloud.path
            #print 'Cloud(registerprocedure):', feed.cloud.registerprocedure
            #print 'Cloud(protocol):', feed.cloud.protocol

        self.entries_result = ''
        self.entries = self.content.entries
        for entry in range(0, self.MAX_ENTRIES):
            current_entry = self.content.entries[entry]
            #print 'Entry:', current_entry.title
            try:
                self.entries_result = str(self.entries_result) + str(current_entry.title) + '\n\n' + str(current_entry.description[:100]) + '...\n'
            except UnicodeEncodeError, e:
                print 'Error: unicode encode', e
            #print 'Description:', current_entry.description
            #if hasattr(current_entry, 'published'):
            #    print current_entry.published
            #if hasattr(current_entry, 'published_parsed'):
            #    print current_entry.published_parsed
            #print 'Updated:', current_entry.updated
           # print 'Updated(parsed):', current_entry.updated_parsed
            #if hasattr(current_entry, 'content'):
            #    print current_entry.content
            #    print current_entry.content.type
            #    print current_entry.content.base
            #    print current_entry.content.language
             #   print current_entry.content.value
            
            #if hasattr(current_entry, 'summary'):
            #    print 'Summary:', current_entry.summary
                 
            #if hasattr(current_entry, 'enclosures'):
            #    print 'Enclosures:', current_entry.enclosures
                
            #if hasattr(current_entry, 'contributors'):
            #    print 'Contributors:', current_entry.contributors
                # name, mail, href (tuple)

            #print 'Id:', current_entry.id
            #print 'Link:', current_entry.link
            #print
           
#data = 'http://webpub.esi.uclm.es/actualidad/noticias.rss' 
#news_reader = NewsReader(data)
#news_reader.render()