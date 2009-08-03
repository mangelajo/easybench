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

import re
import settings

def get_filename(url):
    parts=url.split("/")
    return parts[len(parts)-1]

#
# do_replacements
#
#  replace all the %%str%% macros in the conf_str, if new macros are introduced
# resolve them recursively.
#

def do_replacements(conf_str,server):
    
    replacements = re.findall("%%(\w+)%%",conf_str)
    
    for replacement in replacements:
        replacement_str = "%%"+replacement+"%%"
        replacement_data =""
        
        try:
            replacement_data = settings.CONF_REPLACEMENTS[replacement]
        except:
            replacement_data = server[replacement]
            
        conf_str = conf_str.replace(replacement_str,replacement_data)
    
    # resolve all new macros
    
    if conf_str.find("%%")>=0:
        conf_str = do_replacements(conf_str,server)
   
        
    return conf_str



def print_banner(str_banner, server):
    return