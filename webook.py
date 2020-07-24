
from metaL import *

import flask

class Net(Object):
    pass
class Ip(Net):
    pass
class Port(Net):
    pass

class Web(Net):
    def __init__(self, V):
        Object.__init__(self, V)
        self['host'] = Ip('127.0.0.1')
        self['port'] = Port(12345)
        self.app = flask.Flask(self.val)
        self.app.config['SECRET_KEY'] = os.urandom(32)

    def eval(self, ctx):
        self.app.run(debug=True,
                     host=self['host'].val, port=self['port'].val)


web = vm['web'] = Web(vm)
web.eval(vm)
