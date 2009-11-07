import wordnik
import optparse
import ConfigParser
import textwrap
import sys

if __name__ == '__main__' :
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config", help="path to an ini config file")
    parser.add_option("-w", "--word", dest="word", help="the word you are looking up")
    parser.add_option("-a", "--action", dest="action", help="what would you like to do with this word?", default=None)        

    (opts, args) = parser.parse_args()
    
    cfg = ConfigParser.ConfigParser()
    cfg.read(opts.config)
    
    api_key = cfg.get('wordnik', 'api_key')

    try :
        w = wordnik.wordnik(api_key)
        rsp = w.execute_request('word', opts.word, opts.action)
    except Exception, e:

        print "Wordnik API call failed: %s" % e
        sys.exit()

    if opts.action == 'definitions' :

        for d in rsp :

            try :
                print "[%s] (%s) %s" % (d['@id'], d['partOfSpeech'], d['defTxtSummary'])
            except Exception, e :
                print "[%s] (?) %s" % (d['@id'], d['defTxtSummary'])

    elif opts.action == 'examples' :

        for e in rsp :

            print "# %s" % e['title']
            
            if e.has_key('url') :
                print "# %s" % e['url']

            print ""

            txt = "\"%s\"" % e['display']
            
            print textwrap.fill(txt, 80, initial_indent="\t", subsequent_indent="\t")
            print ""

    elif opts.action == 'frequency' :

        for f in rsp['frequency'] :
            print "[%s] %s" % (f['year'], f['count'])
            
    else :

        for row in rsp :
            try :
                print "[%s] %s" % (rsp['id'], rsp['word'])
            except Exception, e :
                print row
