
DEFAULT_MAKE_OPTS="-j 3"
DEFAULT_CONFIGURE_SETTINGS = "--localstatedir=%%LOCALSTATE%% --prefix=%%PREFIX%%/%%name%% --sysconfdir=%%SYSCONFDIR%% --with-wwwroot=%%WWW_ROOT%%"
DEFAULT_GETMEM="ps --no-headers  -eo comm,rss | grep %s | grep -v grep | grep -v defunct | grep -v zombie | awk '{ print $2 }' - |(tr '\n' +; echo 0) | bc"

NGINX=	 {	"name"		:"nginx",
		"source"	:"http://sysoev.ru/nginx/nginx-0.8.7.tar.gz",
		"version"	:"0.8.7",
                "configure_settings": "--prefix=%%PREFIX%%/%%name%%",
                "copy_sources":True,  # nginx uses a non-standard configure that doesn't work in a build directory
                "makeopts":DEFAULT_MAKE_OPTS,
                "getmem": (DEFAULT_GETMEM % "nginx"),
                "start":  "env PHP_FCGI_CHILDREN=200 PHP_FCGI_MAX_REQUESTS=2000000000 /opt/benchmark/phpcgi/bin/php-cgi -q -b 127.0.0.1:9000 &"
                          "cp conf_templates/nginx-0.8.7/nginx.%(config)s.conf /opt/benchmark/nginx/conf &&"
                          "/opt/benchmark/nginx/sbin/nginx -c conf/nginx.%(config)s.conf",
                "stop":   "killall nginx; killall php-cgi;rm -rf /opt/benchmark/nginx/logs/*"} 
	
LIGHTTPD={	"name"		:"lighttpd",
		"source"	:"http://www.lighttpd.net/download/lighttpd-1.4.23.tar.gz",
		"version"	:"1.4.23",
                "configure_settings": DEFAULT_CONFIGURE_SETTINGS,
                "copy_sources":False,
                "makeopts":DEFAULT_MAKE_OPTS,
                "postinstall"   : ["rm -rf %%PREFIX%%/%%name%%/var && mkdir %%PREFIX%%/%%name%%/var",
                                   "rm -rf %%PREFIX%%/%%name%%/log && mkdir %%PREFIX%%/%%name%%/log"],
                "getmem": (DEFAULT_GETMEM % "lighttpd"),
                "start":  "/opt/benchmark/lighttpd/sbin/lighttpd -f conf_templates/lighttpd-1.4.23/lighttpd.%(config)s.conf",
                "stop":   "killall lighttpd; rm -f /opt/benchmark/lighttpd/log/*"}

CHEROKEE={	"name"		:"cherokee",
		"source"	:"http://www.cherokee-project.com/download/0.99/0.99.22/cherokee-0.99.22.tar.gz",
		"version"	:"0.99.22",
                "configure_settings": DEFAULT_CONFIGURE_SETTINGS+" " + "--enable-static-module=file,fcgi --enable-nls=no",
                "copy_sources":False,
                "makeopts":DEFAULT_MAKE_OPTS,
                "getmem": (DEFAULT_GETMEM % "cherokee"),
                "start":  "/opt/benchmark/cherokee/sbin/cherokee -C conf_templates/cherokee-0.99.20/cherokee.%(config)s.conf -d",
                "stop":   "killall cherokee"}


APACHE=	 {	"name"		:"apache",
		"source"	:"http://www.axint.net/apache/httpd/httpd-2.2.12.tar.gz",
		"version"	:"2.2.12",
                "configure_settings": DEFAULT_CONFIGURE_SETTINGS + \
                    " --enable-so --enable-cgi --enable-info --enable-rewrite --enable-speling --enable-usertrack " +	\
                    "--enable-deflate --enable-ssl --enable-mime-magic",
                "copy_sources":False,
                "makeopts":"",
                "getmem": (DEFAULT_GETMEM % "httpd"),
                "start":  "cp conf_templates/httpd-2.2.12/httpd.%(config)s.conf /opt/benchmark/apache/etc && /opt/benchmark/apache/bin/httpd -f etc/httpd.%(config)s.conf",
                "stop":   "killall httpd"} # no concurrent make for apache, libapr fails on a -j 3 build

APACHE_WORKER={	"name"		:"apache-worker",
                "subbuild_dir":"apache-worker",  
		"source"	:"http://www.axint.net/apache/httpd/httpd-2.2.12.tar.gz",
		"version"	:"2.2.12",
                "configure_settings": DEFAULT_CONFIGURE_SETTINGS + \
                    " --enable-so --enable-cgi --enable-info --enable-rewrite --enable-speling --enable-usertrack " +	\
                    "--enable-deflate --enable-ssl --enable-mime-magic --with-mpm=worker"
                ,
                "copy_sources":False,
                "makeopts":"",
                "getmem": (DEFAULT_GETMEM % "httpd"),
                "start":  "cp conf_templates/httpd-2.2.12/httpd.%(config)s.conf && /opt/benchmark/apache-worker/etc && /opt/benchmark/apache-worker/bin/httpd -f etc/httpd.%(config)s.conf",
                "stop":   "killall httpd"} # no concurrent make for apache, libapr fails on a -j 3 build


PHP=     {      "name"          :"phpmodule",
                "source"        :"http://es.php.net/distributions/php-5.3.0.tar.bz2",
                "version"       :"5.3.0",
                "configure_settings":
                    "--with-apxs2=%%PREFIX%%/apache/bin/apxs --prefix=%%PREFIX%%/apache/php",
                "poststeps":["cp -p php.ini-recommended %%PREFIX%%/apache/php/php.ini"], # installation is missing
                "copy_sources":False,
                "makeopts":DEFAULT_MAKE_OPTS}

PHPCGI=     {   "name"          :"phpcgi",
                "subbuild_dir"  :"phpcgi",
                "source"        :"http://es.php.net/distributions/php-5.3.0.tar.bz2",
                "version"       :"5.3.0",
                "configure_settings":"--prefix=%%PREFIX%%/%%name%%",
                "copy_sources":False,
                "makeopts":DEFAULT_MAKE_OPTS,
                "getmem": (DEFAULT_GETMEM % "php-cgi"),
	        "start":"",
                "stop":"killall php-cgi"}

# list of servers that can be benchmarked
SERVERS=(NGINX,LIGHTTPD,CHEROKEE,APACHE_WORKER)

# list of daemons that where we can start/stop/getmem
SERVER_DAEMONS=(NGINX,LIGHTTPD,CHEROKEE,APACHE_WORKER,PHPCGI)

# list of modules/servers to be built
TO_BUILD=(NGINX,LIGHTTPD,CHEROKEE,APACHE,PHP,PHPCGI,APACHE_WORKER)

#
# archive/source/build directory definitions
#
ARCHIVE_DIR="archive"
SOURCE_DIR="src"
BUILD_DIR="build"

DIRECTORIES=[ARCHIVE_DIR,SOURCE_DIR,BUILD_DIR]

#
# system run/install directories for configure_settings_replacement
#
# pre: directories can't have spaces

WWW_DIR         ="%%PREFIX%%/www"

INSTALL_PREFIX  ="/opt/benchmark"
SYSCONFDIR      ="/opt/benchmark/%%name%%/etc"
WWW_ROOT        ="/opt/benchmark/%%name%%/www"
LOCALSTATE      ="/opt/benchmark/%%name%%/var"

CONF_REPLACEMENTS = {"PREFIX":INSTALL_PREFIX, "SYSCONFDIR":SYSCONFDIR,
                     "WWW_ROOT":WWW_ROOT, "LOCALSTATE":LOCALSTATE}


# generic build options for all projects



