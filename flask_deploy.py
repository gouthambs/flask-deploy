# -*- coding: utf-8 -*-
'''
    flask.ext.deploy
    ----------------

    This module provides wrappers around various production servers
    to ease Flask app deployment.

    :copyright: (c) 2014 by Gouthaman Balaraman
    :license: MIT, see LICENSE for more details.
'''



class WebServer(object):
    def __init__(self,app,host,port, base_url, debug, reloader):
        self.app = app
        self.host = host
        self.port = port
        self.base_url = base_url
        self.debug = debug
        self.reloader = reloader
        self.server = None
        
        
class GeventServer(object):

    def __init__(self, app):
        self.app = app
        self.server = None

    def start(self):
        from gevent import wsgi
        self.server = wsgi.WSGIServer(('', 8088), self.app)
        self.server.serve_forever()

    def stop(self):
        self.server.stop()


class FlaskDebugServer(WebServer):
    def __init__(self, app,host='0.0.0.0', port=8000,base_url='/', debug=False, reloader=False):
        super(self.__class__,self).__init__(app,host,port,base_url,debug,reloader)

    def start(self):
        app.run(self.host, self.port, self.debug, reloader=self.reloader)

    def stop(self):
        pass


class FapwsServer(WebServer):
    def __init__(self, app,host='0.0.0.0', port=8000,base_url='/', debug=False, reloader=False):
        super(self.__class__,self).__init__(app,host,port,base_url,debug,reloader)

    def start(self):
        import fapws._evwsgi as evwsgi
        from fapws import base
        self.server = evwsgi
        self.server.start(self.host,str(self.port))
        self.server.set_base_module(base)
        self.server.wsgi_cb((self.base_url,self.app))
        self.server.set_debug(self.debug)
        self.server.run()

    def stop(self):
        pass
