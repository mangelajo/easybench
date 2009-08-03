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
from helpers import *

def extract_sources(server_s):

	#
	# If we receive a list of server definitions iterate extracting all of them
	#
	if type(server_s)==tuple:
		
		for server in server_s:
			extract_ok = extract_sources(server)
			if not	extract_ok:
				print "[%s] extraction failed, %s/%s" % \
                                    (server["name"], settings.ARCHIVE_DIR, server["source"])
                                return False
                
		return True
	#
	# Check & extract server sources
	#
		
	url = server_s["source"]
	filename = get_filename(url)
	local_filename = settings.ARCHIVE_DIR +"/"+filename

        source_dir = settings.SOURCE_DIR +"/"+ (filename.replace(".tar.gz","").replace(".tar.bz2",""))
        server_s["source_dir"]=source_dir
        
        try:
            os.makedirs(settings.SOURCE_DIR)
        except:
            pass

	if not os.path.exists(source_dir):
                print "extracting files for",source_dir
                
                tar_params = "xvf"
                
                if local_filename.endswith(".tar.bz2"):
                    tar_params +="j"    
                elif local_filename.endswith(".tar.gz"):
                    tar_params +="z"
                
                call_list = ["tar",tar_params,local_filename,"-C",settings.SOURCE_DIR]
		result=call(call_list)
                if result!=0:
                    return False
	
	return True
