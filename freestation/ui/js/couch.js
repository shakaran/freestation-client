/*
JavaScript port of Python3 `microfiber` CouchDB adapter:

    https://launchpad.net/microfiber

This takes inpiration from the CoffeeScript port by Richard Lyon (aka
"richthegeek"):

  http://bazaar.launchpad.net/~dmedia/dmedia/trunk/view/head:/dmedia/webui/data/microfiber.coffee

Rather than inventing an API, this is a simple adapter for calling a REST JSON
API like CouchDB.  The goal is to make something that doesn't need constant
maintenances as additional features are added to the CouchDB API.

For some good documentation of the CouchDB REST API, see:

    http://docs.couchone.com/couchdb-api/

Examples:

>>> var server = new couch.Server('/');
>>> server.put(null, 'mydb');  // Create database 'mydb'
{ok: true}
>>> var database = couch.Database('mydb', '/');  // One way
>>> var database = server.database('mydb');  // Or another, does same thing
>>> var doc = {foo: 'bar'};
>>> database.save(doc);  // POST to couch, update doc _id & _rev in place
{ok: true, id: '2c370303', rev: '1-7a00dff5'}
>>> doc
{_id: '2c370303', _rev: '1-7a00dff5', foo: 'bar'}
>>> database.post(null, '_compact');  // Compact db 'mydb'
{ok: true}
>>> server.post(null, ['mydb', '_compact']);  // Same as above
{ok: true}

*/

"use strict";


var couch = {
    B32ALPHABET: '234567ABCDEFGHIJKLMNOPQRSTUVWXYZ',

    time: function() {
        /* Return Unix-style timestamp like time.time() */
        return Date.now() / 1000;
    },

    random_b32: function() {
        return couch.B32ALPHABET[Math.floor(Math.random() * 32)];
    },

    random_id: function(count) {    
        count = count || 24;
        var letters = [];
        var i;
        for (i=0; i<count; i++) {
            letters.push(couch.random_b32());
        }
        return letters.join('');
    },

    random_id2: function() {
        return [Math.floor(couch.time()), couch.random_id(16)].join('-');
    },
}


couch.errors = {
    400: 'BadRequest',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'NotFound',
    405: 'MethodNotAllowed',
    406: 'NotAcceptable',
    409: 'Conflict',
    412: 'PreconditionFailed',
    415: 'BadContentType',
    416: 'BadRangeRequest',
    417: 'ExpectationFailed',
}


couch.CouchRequest = function(Request) {
    var Request = Request || XMLHttpRequest;
    this.req = new Request();
}
couch.CouchRequest.prototype = {

    on_readystatechange: function() {
        if (this.req.readyState == 4) {
            this.callback(this);
        }
    },

    request: function(callback, method, url, obj) {
        this.callback = callback;
        var self = this;
        this.req.onreadystatechange = function() {
            self.on_readystatechange();
        }
        this.do_request(true, method, url, obj);
    },

    request_sync: function(method, url, obj) {
        this.do_request(false, method, url, obj);
    },

    do_request: function(async, method, url, obj) {
        this.req.open(method, url, async);
        this.req.setRequestHeader('Accept', 'application/json');
        if (method == 'POST' || method == 'PUT') {
            this.req.setRequestHeader('Content-Type', 'application/json');
            if (obj) {
                this.req.send(JSON.stringify(obj));
            }
            else {
                this.req.send();
            }
        }
        else {
            this.req.send();
        }
    },

    read: function() {
        if (!this.req.status) {
            throw 'RequestError';
        }
        if (this.req.status >= 500) {
            throw 'ServerError';
        }
        if (this.req.status >= 400) {
            var error = couch.errors[this.req.status];
            if (error) {
                throw error;
            }
            throw 'ClientError';
        }
        if (this.req.getResponseHeader('Content-Type') == 'application/json') {
            return JSON.parse(this.req.responseText);
        }
        return this.req.responseText;
    },

    abort: function() {
        this.req.abort();
        this.req = null;
    },
}


couch.ChangesMonitor = function(callback, db, since) {
    this.callback = callback;
    this.db = db;
    this.since = since;
    this.monitor();
}
couch.ChangesMonitor.prototype = {
    monitor: function() {
        var self = this;
        var callback = function(r) {
            self.on_request(r);
        }
        this.req = this.db.get(callback, '_changes', 
            {feed: 'longpoll', include_docs: true, since: this.since}
        ); 
    },

    on_request: function(req) {
        var result = req.read();
        if (result.last_seq != this.since) {
            this.since = result.last_seq;
            this.callback(result);
        }
        this.monitor();
    },
}


// microfiber.CouchBase
couch.CouchBase = function(url, Request) {
    this.url = url || '/';
    if (this.url[this.url.length - 1] != '/') {
        this.url = this.url + '/';
    }
    this.basepath = this.url;
    this.Request = Request || XMLHttpRequest;
}
couch.CouchBase.prototype = {
    path: function(parts, options) {
        /*
        Construct a URL relative to this.basepath.

        Examples:

        >>> var inst = new couch.CouchBase('/foo/');
        >>> inst.path();
        '/foo/'
        >>> inst.path('bar');
        '/foo/bar'
        >>> inst.path(['bar', 'baz']);
        '/foo/bar/baz'
        >>> inst.path(['bar', 'baz'], {attachments: true});
        '/foo/bar/baz?attachments=true'

        */
        if (!parts) {
            var url = this.basepath;
        }
        else if (typeof parts == 'string') {
            var url = this.basepath + parts;
        }
        else {
            var url = this.basepath + parts.join('/');
        }
        if (options) {
            var keys = Object.keys(options);
            if (keys.length == 0) {
                return url;
            }
            keys.sort();
            var query = [];
            keys.forEach(function(key) {
                if (options[key] === undefined) {
                    return;
                }
                if (['key', 'startkey', 'endkey'].indexOf(key) > -1) {
                    var value = JSON.stringify(options[key]);
                }
                else {
                    var value = options[key];
                }
                query.push(
                    encodeURIComponent(key) + '=' + encodeURIComponent(value)
                );
            });
            return url + '?' + query.join('&');
        }
        return url;
    },

    request: function(callback, method, obj, parts, options) {
        var url = this.path(parts, options);
        var req = new couch.CouchRequest(this.Request);
        req.request(callback, method, url, obj);
        return req;
    },

    request_sync: function(method, obj, parts, options) {
        var url = this.path(parts, options);
        this.req = new couch.CouchRequest(this.Request);
        this.req.request_sync(method, url, obj);
        return this.req.read();
    },

    put: function(callback, obj, parts, options) {
        return this.request(callback, 'PUT', obj, parts, options);
    },

    put_sync: function(obj, parts, options) {
        /*
        Do a PUT request.

        Examples:

        var cb = new couch.CouchBase('/');
        cb.put(null, 'foo');  # create db /foo
        cb.put({hello: 'world'}, ['foo', 'bar']);  # create doc /foo/bar
        cb.put({a: 1}, ['foo', 'baz'], {batch: true});  # with query option

        */
        return this.request_sync('PUT', obj, parts, options);
    },

    post: function(callback, obj, parts, options) {
        return this.request(callback, 'POST', obj, parts, options);
    },

    post_sync: function(obj, parts, options) {
        /*
        Do a POST request.

        Examples:

        var cb = new couch.CouchBase('/');
        cb.post(null, ['foo', '_compact']);  # compact db /foo
        cb.post({_id: 'bar'}, 'foo');  # create doc /foo/bar
        cb.post({_id: 'baz'}, 'foo', {batch: true});  # with query option

        */
        return this.request_sync('POST', obj, parts, options);
    },

    get: function(callback, parts, options) {
        return this.request(callback, 'GET', null, parts, options);
    },

    get_sync: function(parts, options) {
        /*
        Do a GET request.

        Examples:

        var cb = new couch.CouchBase('/');
        cb.get();  # info about server
        cb.get('foo');  # info about db /foo
        cb.get(['foo', 'bar']);  # get doc /foo/bar
        cb.get(['foo', 'bar'], {attachments: true});  # include attachments
        cb.get(['foo', 'bar', 'baz']);  # get attachment /foo/bar/baz
        */
        return this.request_sync('GET', null, parts, options);
    },

    delete: function(callback, parts, options) {
        return this.request(callback, 'DELETE', null, parts, options);
    },

    delete_sync: function(parts, options) {
        /*
        Do a DELETE request.

        Examples:

        var cb = new couch.CouchBase('/');
        cb.delete(['foo', 'bar', 'baz'], {rev: '1-blah'});  # delete attachment
        cb.delete(['foo', 'bar'], {rev: '2-flop'});  # delete doc
        cb.delete('foo');  # delete database
        */
        return this.request_sync('DELETE', null, parts, options);
    },
}


// microfiber.Server
couch.Server = function(url, Request) {
    couch.CouchBase.call(this, url, Request);
}
couch.Server.prototype = {
    database: function(name) {
        /*
        Return a new couch.Database whose base url is this.url + name.
        */
        return new couch.Database(name, this.url, this.Request);
    },
}
couch.Server.prototype.__proto__ = couch.CouchBase.prototype;


// microfiber.Database
couch.Database = function(name, url, Request) {
    /*
    Make requests related to a database URL.

    Examples:

    >>> var db = new couch.Database('dmedia', '/');
    >>> db.url;
    "/"
    >>> db.basepath;
    "/dmedia/"
    >>> db.name;
    "dmedia"

    */
    couch.CouchBase.call(this, url, Request);
    this.basepath = this.url + name + '/';
    this.name = name;
}
couch.Database.prototype = {
    save: function(doc) {
        /*
        Save *doc* to Couch, update *doc* _id and _rev in place.

        Examples:

        >>> var db = new couch.Database('mydb');
        >>> var doc = {foo: 'bar'};
        >>> db.save(doc);
        {ok: true, id: '2c370303', rev: '1-7a00dff5'}
        >>> doc
        {_id: '2c370303', _rev: '1-7a00dff5', foo: 'bar'}

        */
        var r = this.post_sync(doc);
        doc['_rev'] = r['rev'];
        doc['_id'] = r['id'];
        return r;
    },

    bulksave: function(docs) {
        var rows = this.post_sync({docs: docs, all_or_nothing: true}, '_bulk_docs');
        var i;
        for (i in docs) {
            docs[i]['_rev'] = rows[i]['rev'];
            docs[i]['_id'] = rows[i]['id'];
        }
        return rows;
    },

    view: function(callback, design, view, options) {
        return this.get(callback, ['_design', design, '_view', view], options);
    },

    view_sync: function(design, view, options) {
        /*
        Shortcut for making a GET request to a view.

        No magic here, just saves you having to type "_design" and "_view" over
        and over.  This:

            Database.view(design, view, options);

        Is just a shortcut for:

            Database.view(['_design', design, '_view', view], options);
        */
        return this.get_sync(['_design', design, '_view', view], options);
    },

    att_url: function(doc_or_id, name) {
        /*
        Return URL of a document's attachmnet.

        Examples:

        >>> var db = new couch.Database('dmedia');
        undefined
        >>> db.att_url({'_id': 'foo'}, 'thumbnail');
        "/dmedia/foo/thumbnail"
        >>> db.att_url('foo', 'thumbnail');
        "/dmedia/foo/thumbnail"

        The *name* argument defaults to 'thumbnail' if not provided:

        >>> db.att_url('bar');
        "/dmedia/bar/thumbnail"

        >>> db.att_url('bar', 'other');
        "/dmedia/bar/other"

        */
        name = name || 'thumbnail';
        if (doc_or_id instanceof Object) {
            var _id = doc_or_id['_id'];
        }
        else {
            var _id = doc_or_id;
        }
        return this.path([_id, name]);
    },

    att_css_url: function(doc_or_id, name) {
        /*

        Return an attachment URL formatted to be used in CSS.

        For example:

        >>> var db = new couch.Database('foo');
        >>> db.att_css_url('bar', 'baz');
        'url("/foo/bar/baz")'

        The *name* argument defaults to 'thumbnail' if not provided:

        >>> db.att_css_url('bar');
        'url("/foo/bar/thumbnail")'

        */
        var url = this.att_url(doc_or_id, name);
        return ['url(', JSON.stringify(url), ')'].join('');
    },

    monitor_changes: function(callback, since) {
        return new couch.ChangesMonitor(callback, this, since);
    },

}
couch.Database.prototype.__proto__ = couch.CouchBase.prototype;


couch.Session = function(db, callback) {
    this.db = db;
    this.callback = callback;
    this.timeout_id = null;
    this.docs = {};
    this.dirty = {};
    this.session_id = couch.random_id2();
}
couch.Session.prototype = {
    start: function() {
        var self = this;
        var on_docs = function(req) {
            self.on_docs(req);
        }
        this.db.get(on_docs, '_all_docs', {include_docs: true, update_seq: true});
    },

    on_docs: function(req) {
        var result = req.read();
        result.rows.forEach(function(row) {
            var doc = row.doc;
            if (doc._id.slice(0, 1) == '_') {
                return;
            }
            this.docs[doc._id] = doc;
        }, this);
        var _id;
        for (_id in this.docs) {
            this.callback(this.docs[_id]);
        }

        // Now start the changes monitor starting at the current update_seq
        var self = this;
        var on_changes = function(req) {
            self.on_changes(req);
        }
        this.monitor = this.db.monitor_changes(on_changes, result.update_seq);
    },

    on_changes: function(r) {
        r.results.forEach(function(row) {
            var doc = row.doc;
            if (doc._id.slice(0, 1) == '_') {
                return;
            }
            if (doc.session_id == this.session_id) {
                return;
            }
            if (!this.docs[doc._id]) {
                this.docs[doc._id] = doc;
                this.callback(doc);
            }
            else {
                this.docs[doc._id] = doc;
                this.emit(doc);
            }
        }, this);
    },

    on_complete: function(req) {
        this.req = null;
        var rows = req.read();
        rows.forEach(function(row) {
            this.docs[row.id]._rev = row.rev;
        }, this);
        if (this.pending) {
            this.pending = false;
            this.commit();
        }
    },

    get_doc: function(_id) {
        if (!this.docs[_id]) {
            this.docs[_id] = this.db.get_sync(_id);
        }
        return this.docs[_id];
    },

    save: function(doc, no_emit) {
        /*
        Mark *doc* as dirty, will save when Session.commit() is called.

        This will immediately fire the change notification for this doc, and
        this change will be ignore when it is recieved through the changes feed.
        */
        this.dirty[doc._id] = doc;
        doc.session_id = this.session_id;
        if (!this.docs[doc._id]) {
            this.docs[doc._id] = doc;
            this.callback(doc);
        }
        else if (!no_emit) {
            this.emit(doc);
        }
    },

    commit: function() {
        var docs = [];
        var _id;
        for (_id in this.dirty) {
            docs.push(this.dirty[_id]);
        }
        if (docs.length == 0) {
            return;
        }
        if (this.req) {
            this.pending = true;
            return;
        }
        this.dirty = {};
        var self = this;
        var callback = function(req) {
            self.on_complete(req);
        }
        this.req = this.db.post(callback, {docs: docs, all_or_nothing: true}, '_bulk_docs');
    },

    delayed_commit: function() {
        if (this.timeout_id == null) {
            var self = this;
            var callback = function() {
                self.timeout_id = null;
                self.commit();
            }
            this.timeout_id = setTimeout(callback, 500);
        } 
    },

    ids: {},

    subscribe: function(_id, callback, self) {
        /*
        Subscribe to changes on the doc with *_id*.

        For example:

        >>> session.subscribe(doc._id, this.on_changed, this);

        */
        if (! this.ids[_id]) {
            this.ids[_id] = [];
        }
        this.ids[_id].push({callback: callback, self: self});
    },

    emit: function(doc) {
        var handlers = this.ids[doc._id];
        if (handlers) {
            handlers.forEach(function(h) {
                h.callback.call(h.self, doc);
            });
            if (doc._deleted) {
                delete this.ids[doc._id];
            }
        }
    },
}

