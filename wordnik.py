# http://docs.wordnik.com/api/methods

import urllib
import urllib2
import simplejson

class wordnik :

    def __init__ (self, api_key) :

        self.host = 'http://api.wordnik.com/'
        self.endpoint = 'api/'
        
        self.api_key = api_key
        
    def execute_request(self, method, *stuff) :

        enc_method = urllib.quote(method)
        url = self.host + self.endpoint + enc_method + ".json"

        if len(stuff) :

            enc_stuff = []
            
            for thing in stuff :
                if not thing :
                    continue
                
                enc_stuff.append(urllib.quote(thing))

            if len(enc_stuff) :
                url = "%s/%s" % (url, "/".join(enc_stuff))

        data = None
        
        headers = {
            'api_key' : self.api_key,
            }

        try :
            req = urllib2.Request(url, data, headers)
            res = urllib2.urlopen(req)
        except Exception, e :
            raise e

        try :
            json = simplejson.loads(res.read())
        except Exception, e :
            raise e

        return json
