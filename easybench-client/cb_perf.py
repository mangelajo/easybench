#!/usr/bin/env python

import re, sys, subprocess

# Configuration
#
CONCURRENCY_MIN  = 1
CONCURRENCY_MAX  = 1000
CONCURRENCY_STEP = 20

REQUESTS_NUM     = 100000
KEEPALIVE        = True

# Constants
#
CSV_INCLUDES     = ["concurrency", "reqs_ok", "reqs_fails", "reqs_sec", "trans_rate"]

# Code to call ab
#
def run_cb (url, concu,req_num=REQUESTS_NUM):
    if not concu:
        concu = 1
    if type(url)==list:
        url = " ".join(url)

    cmd = "cherokee-benchmark %s -n %d -c %d \"%s\" 2>&1" % (['', '-k '][KEEPALIVE], req_num, concu, url)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.stdout.read()

def parse_cb (output):
    try:
    	ret = {
            "concurrency": re.findall (r"threads +(\d+),", output)[-1],
            "reqs_ok":     re.findall (r"reqs +(\d+)", output)[-1],
            "reqs_fails":  re.findall (r"fails +(\d+)", output)[-1],
            "reqs_sec":    re.findall (r"\(+(\d+) reqs", output)[-1],
            "trans_rate":  str(int(re.findall (r"\(+(\d+) bytes", output)[-1])/1024),
    	}
    except:
        print output
        ret = {"concurrency":0,"reqs_ok":0,"reqs_fails":0,"reqs_sec":0,"trans_rate":0}
	
    print ret
    return ret


def perform_benchmarks (url):
    # Print the header
    print ','.join(CSV_INCLUDES)

    # Run ab and print restuls
    for concu in range(CONCURRENCY_MIN, CONCURRENCY_MAX + CONCURRENCY_STEP, CONCURRENCY_STEP):
        data = parse_cb (run_cb(url, concu))
        print ','.join([data[x] for x in CSV_INCLUDES])

def ab_benchmark(urls,server_c=None,server_name=None,params={},conf="static"):
    
    if params.has_key("concurrency_min"):
        my_CONCURRENCY_MIN  = params["concurrency_min"]
    else:
        my_CONCURRENCY_MIN  = CONCURRENCY_MIN
     
    if params.has_key("concurrency_max"):   
        my_CONCURRENCY_MAX  = params["concurrency_max"]
    else:
        my_CONCURRENCY_MAX = CONCURRENCY_MAX
        
    if params.has_key("concurrency_step"):
        my_CONCURRENCY_STEP = params["concurrency_step"]
    else:
        my_CONCURRENCY_STEP = CONCURRENCY_STEP
    
    if type(urls)!=list:
        urls = [urls]
    
    results_all = {}
    
    for url in urls:
        results = {}

        if not server_c.start(server_name,conf):
            return {}
        
        print "waking up server....."
        run_cb(url, 100,2000) # wake up!! :)
        
        
        for concu in range(my_CONCURRENCY_MIN, my_CONCURRENCY_MAX + my_CONCURRENCY_STEP, my_CONCURRENCY_STEP):
            print "running to",url,"concurrency",concu
            data = parse_cb (run_cb(url, concu))
            
            
            data["memory_kb"]=server_c.getmem(server_name)
            if conf=="php":
		data["memory_kb"]=data["memory_kb"]+server_c.getmem("phpcgi")     
            results[concu]=data
            print ','.join([data[x] for x in CSV_INCLUDES]),"mem=",data["memory_kb"]
        results_all[url]=results
        
        server_c.stop(server_name)
        
    return results_all
    
