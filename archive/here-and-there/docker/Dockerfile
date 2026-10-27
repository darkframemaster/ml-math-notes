# This is a comment
# Every command must start with word in capital: INSTRUCTION statement

# FROM appoint the source image's name
# MAINTAINER appoint the maintainer of the image
FROM ubuntu:14.04
MAINTAINER Kate Smith <ksmith@example.com>

# RUN will execute a command in the source image
RUN apt-get update && apt-get install -y ruby ruby-dev
RUN gem install sinatra

# Run `docker build` command to build a new image use this dockerfile
# Check `docker build --help` for more detial of `docker build`
