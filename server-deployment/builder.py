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
#
# Helpers
#
   
def build_configure_settings(server):
    conf_str = do_replacements(server["configure_settings"],server)        
    return conf_str.split(" ") # this won't work correctly if directories have spaces
    
#
# Build sources
#

def build_sources(server_s,reconfigure_forced=False):

    #
    # If we receive a list of server definitions iterate building all of them
    #
    if type(server_s)==tuple:
        for server in server_s:
            extract_ok = build_sources(server)
            if not extract_ok:
                print "[%s] build failed" % server["name"]
                return False
        return True

    #
    # Build server sources
    #
    
    print_banner("BUILDING",server_s)

    #
    # Get filename from server source, and build local filename
    #
    url = server_s["source"]
    filename = get_filename(url)
    local_filename = settings.ARCHIVE_DIR +"/"+filename

    #
    # If it's an special build for some package it should have a subdirectory
    # for it's own build (this could be improved, but it's ok)
    #
    subbuild_dir = ""
    
    if server_s.has_key("subbuild_dir"):
        subbuild_dir = server_s["subbuild_dir"] +"/"


    #
    # setup the building directory for this package version
    #
    build_dir = settings.BUILD_DIR +"/"+ subbuild_dir + (filename.replace(".tar.gz","").replace(".tar.bz2",""))
    
    server_s["build_dir"] = build_dir
        
    #
    # make the directory if it doesn't exist
    #
    try:
        os.makedirs(build_dir)
    except:
        pass

    #
    # save the current working directory, and do the build
    #
    SAVED_CWD = os.getcwd()
    
    # if configure_done exists and reconfigure isn't forced do the configure
    
    if (not os.path.exists(build_dir+"/configure_done")) or reconfigure_forced:
        print "configuring build at",build_dir
        
        try:
            os.remove(build_dir+"/configure_done")
        except:
            pass
        
        source_dir = SAVED_CWD +"/"+server_s["source_dir"]
        
        #
        # Some packages don't support to ./configure in a different directory
        # from sources
        #
        
        if server_s["copy_sources"]:
            if call(["cp","-rf",source_dir+"/",settings.BUILD_DIR])!=0:
                print "error copying sources to",build_dir
                return False
        #
        # Change to the build directory, and do the job! ;)
        #
        os.chdir(build_dir)
        
        configure_params = [source_dir+"/configure"]
        configure_params.extend(build_configure_settings(server_s))
        
        print " ".join(configure_params)
        
        print os.getcwd()
        
        result=call(configure_params)
        if result!=0:
            return False
        #
        # Mark the configure as correctly done
        #
        
        f = open("configure_done","w")
        f.write("1\n")
        f.close();
        
        os.chdir(SAVED_CWD)
    #
    # Is the make already done?
    #
        
    if not os.path.exists(build_dir+"/all_done"):
        
        os.chdir(build_dir)
        
        try:
            os.remove(build_dir+"/all_done")
        except:
            pass
        
        make_params=["make"]
        
        # if we have special make options add them to the cmdline
        
        if server_s["makeopts"]!="":
            make_params.extend(server_s["makeopts"].split(" "))
        
        print " ".join(make_params)
        
        result = call(make_params)
        if result!=0:
            print "error doing a", make_params
            return False
        
        #
        # If everything was ok, do the make install
        #
        
        make_params.extend(["install"])
    
        print " ".join(make_params)
        result = call(make_params)
        if result!=0:
            print "error doing a", make_params
            return False
        #
        # do postbuild steps needed for some servers 
        #
            
	if server_s.has_key("postinstall"):
		for post in server_s["postinstall"]:
			post = do_replacements(post,server_s)	
			result = call (post,shell=True)
			if result!=0:
				print "error postinstall => ",post
				return False
    
        #
        # mark build directory as "all done"
        #
        
        f = open("all_done","w")
        f.write("1\n")
        f.close();
        
        os.chdir(SAVED_CWD)
        
    return True
