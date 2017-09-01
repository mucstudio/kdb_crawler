# kdb_crawler

How can I run Firefox on CentOS 7 minimal with no display?
```
yum install firefox
yum install xorg-x11-server-Xvfb
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1

cp geckodriver /usr/bin/
```
