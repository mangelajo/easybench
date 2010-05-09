#!/usr/bin/env python

import out_2 as out_1
from mako.template import Template
from mako.lookup import TemplateLookup
import simplejson as json
import settings

# mylookup = TemplateLookup(directories=[''])
# mytemplate = Template(filename='templates/basic.html',lookup=mylookup)
# print mytemplate.render(servers=["apache","nginx"])



#>>> 
#>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
#'["foo", {"bar": ["baz", null, 1.0, 2]}]'
#>>> str = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
#>>> json.loads(str)
#[u'foo', {u'bar': [u'baz', None, 1.0, 2]}]




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
#   benchresult[0]['servers']=['cherokee','nginx','lighttpd','apache']
#   benchresult[0]['x_axis']="Concurrent Clients"
#   benchresult[0]['x_values']=[1,51,101,151,201,...]
#   benchresult[0]['servers']=[cherokee,nginx,lighttpd,apache]
#   benchresult[0]['configs']=['static','php']

def convert_data(benchmark_data):
    
    benchmark_keys = benchmark_data.keys()
    
    server_conf_stats = {}
    
    for key in benchmark_keys:
        (server,conf) = key.split("_")
            
        if not server_conf_stats.has_key(server):
            server_conf_stats[server] ={}
        
        if len(benchmark_data[key].keys())>0:
            server_conf_stats[server][conf]=benchmark_data[key]
    return server_conf_stats
    
    
def jsName(nm):
    return nm.replace("-","_")
    
def result_write(benchmark_data):
    
    f_json = open(settings.OUTPUT_DIRECTORY+"/data.json","w")
    benchmark_data = convert_data(benchmark_data)
    
    servers = benchmark_data.keys()
    
    global_confs = []
    global_servers = []
    
    for server in servers:
        f_json.write(jsName(server)+ " = new Object;\n")
        f_json.write("%s.name= \"%s\";\n"%(jsName(server),jsName(server)))
        
    
    for server in servers:
        server_benchmark = benchmark_data[server]
        confs = server_benchmark.keys()
        
        if len(confs)>0 and not (servers in global_servers):
                global_servers.append(server)
                
        for conf in confs:
            
            if not (conf in global_confs):
                global_confs.append(conf)
            f_json.write(jsName(server)+"."+jsName(conf)+" = new Object;\n")
            
            config_benchmark = server_benchmark[conf]
            urls = config_benchmark.keys()
            
            print server,conf,urls
            
            i = 0
            
            for url in urls:
                
                url_benchmark = config_benchmark[url]
                bench = {}
                bench['type']="x/clients"
                bench['x_axis']="clients"
                bench['test_urls']=url
                
                bench['x_axis_values'] = []
                
                bench['concurrency'] = []
                bench['reqs_sec'] = []
                bench['reqs_ok']  = []
                bench['reqs_fails'] =[]
                bench['memory_kb'] =[]
                bench['trans_rate'] =[]
                
                x_axis_values = url_benchmark.keys()
                x_axis_values.sort()
                for x_axis in x_axis_values:
                    b_data = url_benchmark[x_axis]
                    
                    bench['x_axis_values'].append(x_axis)
                    for b_data_key in b_data.keys():
                        
                        bench[b_data_key].append(b_data[b_data_key])
                
                json_dump = json.dumps(bench)
                
                f_json.write("%s.%s[%d]="%(jsName(server),jsName(conf),i))
                f_json.write(json_dump+";\n")
                
                i = i +1
                
    f_json.write("confs = [")
    for conf in global_confs:
        f_json.write('"'+jsName(conf)+'"')
        if conf!=global_confs[len(global_confs)-1]:
            f_json.write(",")
    
    f_json.write("];\n")
    
    f_json.write("servers = [")
    for server in global_servers:
        f_json.write(jsName(server))
        if server!=servers[len(servers)-1]:
            f_json.write(",")
    
    f_json.write("];\n")    
    


    
    
result_write(out_1.server)
