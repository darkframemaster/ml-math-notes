# opencv
...

##install in ubuntu 2015.04
[download opencv](http://opencv.org)

`sudo apt-get install build-essential libgtk*-dev libavcodec-dev libavformat-dev libjepg-dev libtiff*-dev cmake libswscale-dev libjasper-dev`

`cmake .`

**wait...**

`make`

`sudo make install`

**config library:**

`cd /etc/ld.so.conf.d`

`su`

`touch opencv.conf`

`echo "/usr/local/lib" >> opencv.conf`

`ldconfig`

`echo "PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig" >> /etc/bash.bashrc`

`echo "export PKG_CONFIG_PATH" >> /etc/bash.bashrc`

`exit`

**test:**

`cd /PATH/TO/OPENCV/samples/cpp/example_cmake`

`make`

`./opencv_example`

**makefile**

using command:

>g++ main.cpp -o main `pkg-config --cflags --libs opencv`

or cmake(CMakeList.txt):

`cmake_minimum_required(VERSION 2.8)`

`project(Hello)`

`find_package(OpenCV REQUIRED)`

`add_executable(Hello main.cpp)`

`target_link_libraries(Hello ${OpenCV_LIBS})`

## Run example
unpacking `objectDetection.zip` and run the example.

##enjoy your opencv！
[help](www.douban.com/note/478450231)
