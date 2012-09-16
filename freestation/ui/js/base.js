"use strict";

/*
A very minimal "unframework" to capture just a few important patterns, make a
few things nicer, less verbose.  But this is *not* a band aid for browser
compatibility, nor for the JavaScript language.

Note that couch.js should never depend on anything in here.
*/


function $bind(func, self) {
    return function() {
        var args = Array.prototype.slice.call(arguments);
        return func.apply(self, args);
    }
}


function $A(id) {
    /*
    Return the element with id="id".

    If `id` is an Element, it is returned unchanged.

    Examples:

    >>> $('browser');
    <div id="browser" class="box">
    >>> var el = $('browser');
    >>> $(el);
    <div id="browser" class="box">

    */
    if (id instanceof Element) {
        return id;
    }
    return document.getElementById(id);
}


function $el(tag, attributes) {
    /*
    Convenience function to create a new DOM element and set its attributes.

    Examples:

    >>> $el('img');
    <img>
    >>> $el('img', {'class': 'thumbnail', 'src': 'foo.png'});
    <img class="thumbnail" src="foo.png">

    */
    var el = document.createElement(tag);
    if (attributes) {
        var key;
        for (key in attributes) {
            var value = attributes[key];
            if (key == 'textContent') {
                el.textContent = value;
            }
            else {
                el.setAttribute(key, value);
            }
        }
    }
    return el;
}


function $replace(incumbent, replacement) {
    /*
    Replace `incumbent` with `replacement`.

    `incumbent` can be an element or id, `replacement` must be an element.

    Returns the element `incumbent`.
    */
    var incumbent = $(incumbent);
    return incumbent.parentNode.replaceChild(replacement, incumbent);
}


function $prepend(child, parent) {
    /*
    Insert *child* as the first child element in *parent*.
 
    */
    var first = parent.children[0];
    if (first) {
        return parent.insertBefore(child, first);
    }
    return parent.appendChild(child);
}


function $scroll_to(id) {
    var child = $(id);
    if (! (child && child.parentNode)) {
        return;
    }
    var start = child.offsetTop;
    var end = start + child.offsetHeight;
    var vis_start = child.parentNode.scrollTop;
    var vis_end = vis_start + child.parentNode.clientHeight;
    if (start < vis_start) {
        child.parentNode.scrollTop = start;
    }
    else if (end > vis_end) {
        child.parentNode.scrollTop = end - child.parentNode.clientHeight;
    }
}


function $hide(id) {
    var element = $(id);
    if (element) {
        element.classList.add('hide');
        return element;
    }
}


function $show(id) {
    var element = $(id);
    if (element) {
        element.classList.remove('hide');
        return element;
    }
}


function $select(id) {
    var element = $(id);
    if (element) {
        element.classList.add('selected');
        return element;
    }
}


function $unselect(id) {
    var element = $(id);
    if (element) {
        element.classList.remove('selected');
        return element;
    }
}


function time() {
    /* Return Unix-style timestamp like time.time() */
    return Date.now() / 1000;
}


function bytes10(size) {
    /*
    Return *size* bytes to 3 significant digits in SI base-10 units.

    For example:
    >>> bytes10(1000);
    "1 kB"
    >>> bytes10(29481537)
    "29.5 MB"
    >>> bytes10(392012353)
    "392 MB"

    For additional details, see:

        https://wiki.ubuntu.com/UnitsPolicy
    */
    var BYTES10 = [
        'bytes',
        'kB',
        'MB',
        'GB',
        'TB',
        'PB',
        'EB',
        'ZB',
        'YB',
    ];
    if (size == 0) {
        return '0 bytes';
    }
    if (size == 1) {
        return '1 byte';
    }
    var ex = Math.floor(Math.log(size) / Math.log(1000));
    var i = Math.min(ex, BYTES10.length - 1);
    var s = ((i > 0) ? size / Math.pow(1000, i) : size).toPrecision(3);
    if (s.indexOf('.') > 0) {
        var end = s.slice(-1);
        while (end == '0' || end == '.') {
            s = s.slice(0, -1);
            if (end == '.') {
                break;
            }
            end = s.slice(-1);
        }
    }
    return s + ' ' + BYTES10[i];
}


var Hub = {
    /*
    Relay signals between JavaScript and Gtk.

    For example, to send a signal to Gtk via document.title:

    >>> Hub.send('click');
    >>> Hub.send('changed', 'foo', 'bar');

    Or from the Gtk side, send a signal to JavaScript by using
    WebView.execute_script() to call Hub.recv() like this:

    >>> Hub.recv('{"signal": "error", "args": ["oops!"]}');

    Use userwebkit.BaseApp.send() as a shortcut to do the above.

    Lastly, to emit a signal from JavaScript to JavaScript handlers, use
    Hub.emit() like this:

    >>> Hub.emit('changed', 'foo', 'bar');

    */
    i: 0,

    names: {},

    connect: function(signal, callback, self) {
        /*
        Connect a signal handler.

        For example:

        >>> Hub.connect('changed', this.on_changed, this);

        */
        if (! Hub.names[signal]) {
            Hub.names[signal] = [];
        }
        Hub.names[signal].push({callback: callback, self: self});
    },

    send: function() {
        /*
        Send a signal to the Gtk side by changing document.title.

        For example:

        >>> Hub.send('changed', 'foo', 'bar');

        */
        var params = Array.prototype.slice.call(arguments);
        var signal = params[0];
        var args = params.slice(1);
        Hub._emit(signal, args);
        var obj = {
            'i': Hub.i,
            'signal': signal,
            'args': args,
        };
        Hub.i += 1;
        document.title = JSON.stringify(obj);
    },

    recv: function(data) {
        /*
        Gtk should call this function to emit a signal to JavaScript handlers.
        
        For example:

        >>> Hub.recv('{"signal": "changed", "args": ["foo", "bar"]}');

        If you need to emit a signal from JavaScript to JavaScript handlers,
        use Hub.emit() instead.
        */
        var obj = JSON.parse(data);
        Hub._emit(obj.signal, obj.args);
    },

    emit: function() {
        /*
        Emit a signal from JavaScript to JavaScript handlers.

        For example:

        >>> Hub.emit('changed', 'foo', 'bar');

        */
        var params = Array.prototype.slice.call(arguments);
        Hub._emit(params[0], params.slice(1));
    },

    _emit: function(signal, args) {
        /*
        Low-level private function to emit a signal to JavaScript handlers.
        */
        var handlers = Hub.names[signal];
        if (handlers) {
            handlers.forEach(function(h) {
                h.callback.apply(h.self, args);
            });
        }
    },
}

