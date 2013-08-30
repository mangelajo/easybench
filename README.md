Small HTTP benchmarking framework that automatically downloads and builds nginx, lighttpd, apache, cherokee, and php sources.

The idea is to build benchmarks definitions and results that you don't have to trust on because everyone can replicate and tune in easy steps, and everybody can contribute to make them as real as possible.

Introduction
============

Easybench is an small http benchmarking framework. It's designed to download, compile, and run the sourcecode of apache, nginx, lighttpd and cherokee webservers.

At this moment it also downloads php-cgi to test the php-serving speed of every server. It would be really interesting to add ruby and django support to be able to test speed with those web frameworks too.

Infrastructure
--------------

The system is divided in two parts:

server-deployment
-----------------

This part will let you start a server just calling ./go.py . That's not 100% true, because you will have to satisfy all source and library dependencies in your system, an small guide for major distributions will be available in SourceCodeDependencies

This is what ./go.py will do for you:

download sources, make directories
for every server (see settings.py):
* configure
* make
* make install
When build is done it exports an XML-RPC API for remote loading/unloading/changing/tuning configuration files and getting memory usage at runtime.

easybench-client
----------------


This is the client that will let you create nice .html + javascript statistics, they are based in jQuery + flot. As easy as:

run as root:

  # ulimit -n 4096 <-- this is recomended
  
  # ./easybench.py IP

For running the benchmarks it depends on:

b (apache benchmark)
herokee-bench (cherokee benchmark)
In a near future httperf could be used to make more complicated benchmarks.

Limits
------

At this moment only y axis= {XXX} / x axis ={concurrent conections} benchmark type is supported. After some refactorings and versions probably other kind of benchmarks could be supported.


