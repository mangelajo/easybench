#!/usr/bin/env python


RPC_SERVER = "http://%(ip)s:8000/rpc"

URLS={ "php":[
              "http://%(ip)s/index.php",
#              "http://%(ip)s/index2.php"
              ],
    
        "static":
            [
#              "http://%(ip)s/index.html",
#              "http://%(ip)s/rand16.bin",
              "http://%(ip)s/rand64.bin",
              "http://%(ip)s/rand128.bin",
#              "http://%(ip)s/rand512.bin",
#              "http://%(ip)s/rand1024.bin"
              ]}

SERVERS = ["apache","cherokee","apache-worker","nginx","lighttpd"]
#CONFS=["php"]
#SERVERS=["cherokee","apache","apache-worker","nginx","lighttpd"]
CONFS=["static"]

OUTPUT_DIRECTORY = "output"
