class configinfo():
    #输入cookie，例如：cookie='12qhfu3eibzcd...'
    cookie='timeOffset_o=1080.39990234375; smidV2=20221030114400934812eb9d01e5166c455338273f27e0004438feec475e540; testcookie=yes; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1674128360; token=MjY5OTIyODJ8NjU2ZTk2ZDJmZjQ3ZDM4NGIxYjFmNTFhZWY3NTA5MjB8fHx8MjU5MjAwMHwxfHx85pmL5rGf55So5oi3fDB8bW9iaWxlfDF8MHx8; JJSESS=%7B%22returnUrl%22%3A%22https%3A//my.jjwxc.net/login.php%22%2C%22clicktype%22%3A%22%22%2C%22sidkey%22%3A%22wpFN9s8xH2OEWMPSIVTcGfJKzj60aolXBm5q3nU%22%7D; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1675348077; JJEVER=%7B%22shumeideviceId%22%3A%22WC39ZUyXRgdEJqIoGEOjtxdhg5r1gdnRPP8PsD0XnDH5tKw9QIZ69jPdsb45S9jrtoBurBTWKzRaNjVTrDB+vjSSIKg7syaBqtL/WmrP2Tav+DYF2YqyHq3DuF8MxnSrL3fVLMpg6KnIpXaRjNlRoBZ4mCbdPQ1BRajW7hxiYtqOGduzx9VSOobfD5OSmfbqw0JSgM/vzIa0G7wWr0zokq8v37PqS1NZybBQp721OeIn5yRcHOHTURiX6/sHkizuA1487577677129%22%2C%22fenzhan%22%3A%22by%22%2C%22lastCheckLoginTimePc%22%3A1675347977%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E6%259C%2589%25E9%2597%25B2%22%2C%22sms_total%22%3A%220%22%2C%22desid%22%3A%22ItJvHsFm0z2FLzFsNus9AXzG0vA+8ij9%22%2C%22foreverreader%22%3A%2226992282%22%7D'
    #繁简转换标志：繁转简（输入s）；简转繁（输入t）；不变（不输入），例如：state='s'
    state=''
    
    '''
    标题保存状态(序号 章节名称 内容提要)
    显示则输入1，不显示则输入0，数字之间用空格隔开
    例如：若只显示序号和内容提要，则输入'1 0 1'
    '''
    titleInfo='0 1 0'
        
    #线程池最大容量（数字越大，占据内存等资源越多，数字越小，下载越慢，总之看个人电脑状况决定）
    ThreadPoolMaxNum=5
