# kdb_crawler

### How can I run Firefox on CentOS 7 minimal with no display?

```
yum install firefox
yum install xorg-x11-server-Xvfb
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1

cp geckodriver /usr/bin/
```
or

Just install PhantomJS. Then, change this line:

```
driver = webdriver.Firefox()
```
to:
```
driver = webdriver.PhantomJS()
```
The rest of your code won't need to be changed and no browser will open. For debugging purposes, use `driver.save_screenshot('screen.png')` at different steps of your code or just keep using the Firefox webdriver in development.

### crontab
0 1 * * * cd /opt/kdb/kdb_crawler; export DISPLAY=:1; /usr/bin/nohup /opt/python36/bin/scrapy crawl tmall-xpath > /opt/kdb/kdb_crawler/log/`date +\%Y-\%m-\%d` 2>&1 &
