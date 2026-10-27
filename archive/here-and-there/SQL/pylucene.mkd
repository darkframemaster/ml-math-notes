# pylucene
Text search engine.

# install
## install java-8
```bash
$apt-get install software-properties-common
$add-apt-repository ppa:webupd8team/java
$apt update
$apt-get install oracle-java8-installer
Oracle JRE 8 browser plugin installed
Oracle JDK 8 installed
#####Important########
To set Oracle JDK8 as default, install the "oracle-java8-set-default" package.
E.g.: sudo apt install oracle-java8-set-default.
Setting up gsfonts (1:8.11+urwcyr1.0.7~pre44-4.2ubuntu1) ...
Setting up x11-common (1:7.7+1ubuntu8.1) ...
 * Setting up X socket directories...                                                                                                 [ OK ] 
Setting up oracle-java8-set-default (8u111+8u111arm-1~webupd8~0) ...
Processing triggers for ureadahead (0.100.0-16) ...
Setting up xfonts-encodings (1:1.0.4-1ubuntu1) ...
Setting up xfonts-utils (1:7.7+1) ...
Setting up gsfonts-x11 (0.22) ...
Processing triggers for libc-bin (2.19-0ubuntu6.7) ...

#Check if it is installed successful
$java -version
java version "1.8.0_111"
Java(TM) SE Runtime Environment (build 1.8.0_111-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.111-b14, mixed mode)

#Check Java JDK directory `/usr/lib/jvm/java-8-oracle`.
$ls /usr/lib/jvm
java-8-oracle
```

## install pylucene
### Get pylucene
Two ways to download pylucene:

* Get pylucene from http://lucene.apache.org/pylucene/features.html
* Or choise a version from http://mirrors.hust.edu.cn/apache/lucene/pylucene/. For example:`$wget http://mirrors.hust.edu.cn/apache/lucene/pylucene/pylucene-6.2.0-src.tar.gz`

### Install jcc and ant
```bash
$cd <path_to_pylucene>/
$pushd jcc
$vim setup.py	#edit setup.py to match your environment. like your java environment
$python setup.py build
$python setup.py install
running install
running bdist_egg
running egg_info
creating JCC.egg-info
writing JCC.egg-info/PKG-INFO
writing top-level names to JCC.egg-info/top_level.txt
writing dependency_links to JCC.egg-info/dependency_links.txt
writing manifest file 'JCC.egg-info/SOURCES.txt'
reading manifest file 'JCC.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
writing manifest file 'JCC.egg-info/SOURCES.txt'
installing library code to build/bdist.linux-x86_64/egg
running install_lib
running build_py
not writing /home/xuehao/pylucene-6.2.0/jcc/jcc/config.py
running build_ext
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/egg
creating build/bdist.linux-x86_64/egg/jcc
creating build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JCCEnv.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JObject.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/functions.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/types.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JArray.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JArray.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/jcc.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/jccfuncs.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JObject.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/JCCEnv.cpp -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/functions.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/sources/macros.h -> build/bdist.linux-x86_64/egg/jcc/sources
copying build/lib.linux-x86_64-2.7/jcc/cpp.py -> build/bdist.linux-x86_64/egg/jcc
copying build/lib.linux-x86_64-2.7/jcc/config.py -> build/bdist.linux-x86_64/egg/jcc
creating build/bdist.linux-x86_64/egg/jcc/patches
copying build/lib.linux-x86_64-2.7/jcc/patches/patch.4195 -> build/bdist.linux-x86_64/egg/jcc/patches
copying build/lib.linux-x86_64-2.7/jcc/patches/patch.43.0.6c11 -> build/bdist.linux-x86_64/egg/jcc/patches
copying build/lib.linux-x86_64-2.7/jcc/patches/patch.43.0.6c7 -> build/bdist.linux-x86_64/egg/jcc/patches
copying build/lib.linux-x86_64-2.7/jcc/python.py -> build/bdist.linux-x86_64/egg/jcc
copying build/lib.linux-x86_64-2.7/jcc/windows.py -> build/bdist.linux-x86_64/egg/jcc
copying build/lib.linux-x86_64-2.7/jcc/__init__.py -> build/bdist.linux-x86_64/egg/jcc
copying build/lib.linux-x86_64-2.7/jcc/__main__.py -> build/bdist.linux-x86_64/egg/jcc
copying build/lib.linux-x86_64-2.7/jcc/_jcc.so -> build/bdist.linux-x86_64/egg/jcc
byte-compiling build/bdist.linux-x86_64/egg/jcc/cpp.py to cpp.pyc
byte-compiling build/bdist.linux-x86_64/egg/jcc/config.py to config.pyc
byte-compiling build/bdist.linux-x86_64/egg/jcc/python.py to python.pyc
byte-compiling build/bdist.linux-x86_64/egg/jcc/windows.py to windows.pyc
byte-compiling build/bdist.linux-x86_64/egg/jcc/__init__.py to __init__.pyc
byte-compiling build/bdist.linux-x86_64/egg/jcc/__main__.py to __main__.pyc
creating stub loader for jcc/_jcc.so
byte-compiling build/bdist.linux-x86_64/egg/jcc/_jcc.py to _jcc.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying JCC.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying JCC.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying JCC.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying JCC.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
copying JCC.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
writing build/bdist.linux-x86_64/egg/EGG-INFO/native_libs.txt
creating dist
creating 'dist/JCC-2.22-py2.7-linux-x86_64.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)
Processing JCC-2.22-py2.7-linux-x86_64.egg
creating /usr/local/lib/python2.7/dist-packages/JCC-2.22-py2.7-linux-x86_64.egg
Extracting JCC-2.22-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
Adding JCC 2.22 to easy-install.pth file

Installed /usr/local/lib/python2.7/dist-packages/JCC-2.22-py2.7-linux-x86_64.egg
Processing dependencies for JCC==2.22
Finished processing dependencies for JCC==2.22
$popd

# install ant
$apt-get install ant
```

### Eorrors & Solutions
#### Python.h: No such file or directory
It looks like you haven't properly installed the header files and static libraries for python dev. Use your package manager to install them system-wide.

```bash
$apt-get install python-dev
# Or if you are running python3
$apt-get install python3-dev
```

[see also](http://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory)
