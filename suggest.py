import wordnik
import optparse
import ConfigParser
import textwrap
import sys

if __name__ == '__main__' :
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config", help="path to an ini config file")
    parser.add_option("-w", "--word", dest="word", help="the word you would like auto-complete suggestions for")
    parser.add_option("-d", "--definitions", dest="definitions", help="", default=False, action='store_true')
    
    (opts, args) = parser.parse_args()
    
    cfg = ConfigParser.ConfigParser()
    cfg.read(opts.config)
    
    api_key = cfg.get('wordnik', 'api_key')

    try :
        w = wordnik.wordnik(api_key)
        rsp = w.execute_request('suggest', opts.word)
    except Exception, e:

        print "Wordnik API call failed: %s" % e
        sys.exit()

    for m in rsp['match'] :

        print "[%s]\t%s" % (m['frequency'], m['word'])

        if opts.definitions :

            try :
                rsp_d = w.execute_request('word', m['word'], 'definitions')
            except Exception, e :
                print ""
                continue
            
            for d in rsp_d :

                txt = "\"%s\"" % d['defTxtSummary']
                print textwrap.fill(txt, 72, initial_indent="\t", subsequent_indent="\t")

            print ""
