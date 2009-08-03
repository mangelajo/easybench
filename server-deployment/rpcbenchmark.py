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

import os
import os.path
from subprocess import *
import settings
import re
from helpers import *
from settings import SERVER_DAEMONS
import time

def get_server(server_name):
    for server in SERVER_DAEMONS:
        if server["name"]==server_name:
            return server
    
    return None

def server_exec(to_exec, server_name,config=""):
    
    server = get_server(server_name)
    
    if server==None:
        return "UNKNOWN SERVER %s" % server_name
        
    sh = server[to_exec] % {"config":config}
        
    result = call(sh,shell=True)
     
    if result==0:
        return True
    
    return False

class RPCBenchmarkServer:
    
    
    
    def start(self, server_name, config):
        running_server = self.running_server()
        
        if running_server!="NONE":
            self.stop(running_server)
            
            
        
        return server_exec("start",server_name,config)
       
    
    
    def stop(self,server_name):
        res= server_exec("stop",server_name)
        if res:
            time.sleep(4)
        return res
        
    def stop_all(self):
        for server in settings.SERVER_DAEMONS:
            self.stop(server["name"])
        return True
    
    def getmem(self,server_name):
        
        server = get_server(server_name)
    
        
        if server==None:
            return "UNKNOWN SERVER %s" % server_name
        
        sh = server["getmem"]
        p = Popen(sh,shell=True,stdout=PIPE)
        p.wait()
        result = p.communicate()[0]
        return int(result.rstrip("\n"))
        
    def running_server(self):
        for server in settings.SERVER_DAEMONS:
            mem = int(self.getmem(server["name"]))
            if mem>0:
                return server["name"]
            
        return "NONE"
                
    def get_servers(self):
        s_list = []
        for server in settings.SERVERS:
            s_list.append(server["name"])
        
        return s_list
        
    
    

