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
#  * Neither the name of the <ORGANIZATION> nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
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
import os
import os.path
import sys
from download import download_sources
from sources import extract_sources
from builder import build_sources
from testfiles import copy_testfiles

def check_create_dirs(dirs):
	for dir in dirs:
		if not os.path.isdir(dir):
			os.makedirs(dir)


def build_all():

	#
	# pre) create all archive,sources,and build working directories
	#
		
	check_create_dirs(settings.DIRECTORIES)
	
	#
	# 1st) it will download all sources to the ARCHIVE_DIR directory,
	# if it finds any kind of problem exit 1 to system.
	#
	
	if not download_sources(settings.TO_BUILD):
		sys.exit(1)
	
	
	#
	# 2nd) it will extract all sources to the sources directory of 
	# every project, they will be created under the SOURCES_DIR directory
	#
	
	
	if not extract_sources(settings.TO_BUILD):
		sys.exit(2)
		
	
	#
	# 3rd) it will build binaries for every server, they will be built
	# under the BUILD_DIR directory
	#
	
	if not build_sources(settings.TO_BUILD):
		sys.exit(3)
		
	#
	# 4th) Copy all test files to be served
	#

	if not copy_testfiles():
		sys.exit(4)

if __name__ == "__main__":
    build_all()


