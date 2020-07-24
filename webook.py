## @file
## @brief Web Book engine

## @defgroup webook WebBook
## @brief documenting engine /Flask/

from metaL import *

## @defgroup doc Documenting

## @ingroup doc
class Doc(Object):
    pass

## @ingroup doc
## paragraph
class P(Doc):
    pass

## @ingroup doc
class PNG(Doc, File):
    pass

## @ingroup doc
class Color(Doc):
    pass
## @ingroup doc
class Font(Doc):
    pass
## @ingroup doc
class Size(Doc):
    pass

## @ingroup webook
## networking object
class Net(IO):
    pass

## @ingroup webook
## TCP/IP address
class Ip(Net):
    pass

## @ingroup webook
## TCP/IP port
class Port(Net):
    pass


import flask

## @ingroup webook
class Web(Net):
    def __init__(self, V):
        Object.__init__(self, V)
        self['host'] = Ip('127.0.0.1')
        self['port'] = Port(12345)
        self.app = flask.Flask(self.val)
        self.app.config['SECRET_KEY'] = os.urandom(32)

    def eval(self, ctx):

        @self.app.route('/')
        def index():
            return flask.render_template('index.html', vm=vm, web=self, ctx=ctx)

        @self.app.route('/css.css')
        def css():
            return flask.Response(
                flask.render_template('css.css', vm=vm, web=self, ctx=ctx),
                mimetype='text/css')

        @self.app.route('/<path:path>.css')
        def somecss(path):
            return self.app.send_static_file(path + '.css')

        @self.app.route('/<path:path>.png')
        def png(path):
            return self.app.send_static_file(path + '.png')

        @self.app.route('/<path:path>.js')
        def js(path):
            return self.app.send_static_file(path + '.js')

        self.app.run(debug=True, extra_files=sys.argv[1:],
                     host=self['host'].val, port=self['port'].val)


web = vm['web'] = Web(vm)
web << Color('lightgreen')
web['back'] = Color('black')
web['logo'] = PNG('logo.png')
web['font'] = Font('monospace') << Size('5mm')
web.eval(vm)
