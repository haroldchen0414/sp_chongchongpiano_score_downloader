# sp_chongchongpiano_score_downloader
一个获取虫虫钢琴乐谱的程序

[参考来源](https://www.52pojie.cn/thread-1470976-1-1.html)，将其用selenium封装，浏览器使用Chrome

chromedriver.exe下载方法：  
chrome浏览器运行chrome://version/，获取浏览器版本号  
进入页面https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
找到对应浏览器版本的chromedriver下载  
将chongchongpiano_score_downloader.py中的executable_path换成chromedriver的目录

将url换成想要的地址  
运行chongchongpiano_score_downloader.py脚本，会在output文件夹下生成五线谱和简谱的pdf文件



