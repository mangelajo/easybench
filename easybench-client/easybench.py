#!/usr/bin/env python
#
# Copyright (c) 2009, NBEE Embedded Systems S.L. http://www.nbee.es
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of NBEE Embedde Systems S.L. nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import settings
import ab_perf
import sys
import os.path
from xmlrpclib import ServerProxy
from mako.template import Template
from mako.lookup import TemplateLookup
import simplejson as json

# mylookup = TemplateLookup(directories=[''])
# mytemplate = Template(filename='templates/basic.html',lookup=mylookup)
# print mytemplate.render(servers=["apache","nginx"])



#>>> import simplejson as json
#>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
#'["foo", {"bar": ["baz", null, 1.0, 2]}]'
#>>> str = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
#>>> json.loads(str)
#[u'foo', {u'bar': [u'baz', None, 1.0, 2]}]

    

def print_banner(server,conf):

    print "*********************************************************"
    print "                                                         "
    print "               ",server,conf
    print "                                                         "
    print "*********************************************************"

def main():
    
    if len(sys.argv)<2:
        print "usage:"
        print "  ",sys.argv[0]," <ip-address>"
        print ""
        sys.exit(1)
    
    ip = sys.argv[1]
    
    server_c = ServerProxy(settings.RPC_SERVER % {"ip":ip})
    server_c.stop_all()
    
    
    
    stats = {}
    for conf in settings.CONFS:
        
        urls = []
        stats_c ={}
    
        for url in settings.URLS[conf]:
            urls.append(url % {"ip":ip})
            
        
        for server in settings.SERVERS:
            print_banner(server,conf)
        
            
            s_stats = ab_perf.ab_benchmark(urls,server_c,server,{},conf)
            
            print s_stats
            
            stats_c[server]=s_stats
    
        stats[conf]=stats_c 
    


if __name__ == "__main__":
    main()

#
# output:
#   cherokee['static'][0]['type']="x/clients"
#   cherokee['static'][0]['x_axis']="clients"
#   cherokee['static'][0]['test_urls']=[......]
#   cherokee['static'][0]['reqs_sec']=[.....]
#   cherokee['static'][0]['reqs_ok']=[.....]
#   cherokee['static'][0]['reqs_fail']=[.....]
#   cherokee['static'][0]['memory_kb']=[.....]
#   cherokee['static'][0]['transfer_rate']=[.....]
#
#      
#
#   benchresult[0]['servers']=['cherokee','nginx','lighttpd','apache']
#   benchresult[0]['x_axis']="Concurrent Clients"
#   benchresult[0]['x_values']=[1,51,101,151,201,...]
#   benchresult[0]['servers']=[cherokee,nginx,lighttpd,apache]

