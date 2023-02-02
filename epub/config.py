class configinfo():
    #输入cookie，例如：cookie='12qhfu3eibzcd...'
    
    cookie='Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1675345224;JJEVER=%7B%22shumeideviceId%22%3A%22WC39ZUyXRgdEAEiRytfb3Tcj6P7G8Z98CjJ/fzq606Be+hlMoRnL9wAVpNYyxVkWUmZ+VYPeOGIFNxPsSjPzHuzIp82bocfaVtL/WmrP2Tav+DYF2YqyHqx1HqKodCQwh3fVLMpg6KnK+4M2GQH+t5CrW9zmoUZt5ajW7hxiYtqOGduzx9VSOobfD5OSmfbqw0JSgM/vzIa0G7wWr0zokq8v37PqS1NZyHQzkskZRm7pUf4f/H7g7DZoQMnY11jut1487577677129%22%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E6%259C%2589%25E9%2597%25B2%22%2C%22foreverreader%22%3A%2226992282%22%2C%22desid%22%3A%22BztwhmqF8F72F+3mxO+wmuAJCBs8j3S7%22%2C%22sms_total%22%3A0%7D;timeOffset_o=-219.699951171875;token=MjY5OTIyODJ8ZjFjYmU5NWZlOWQ3OTJjNjc2NmI5NTdmNTI5Yzg2YzR8fHx8MjU5MjAwMHwxfHx85pmL5rGf55So5oi3fDB8bW9iaWxlfDF8MHx8;Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1675345179;JJSESS=%7B%22sidkey%22%3A%22oh4VHrUsXl0GxCDneOQ2LuTPvbEkYjwIJ5WAMdy%22%7D;testcookie=yes;__yjs_duid=1_dbd540f4de2f8ef4afe8bc3c3115789f1675345176510'
    
    #繁简转换标志：繁转简（输入s）；简转繁（输入t）；不变（不输入），例如：state='s'
    state=''
    
    '''
    标题保存状态(序号 章节名称 内容提要)
    显示则输入1，不显示则输入0，数字之间用空格隔开
    例如：若只显示序号和内容提要，则输入'1 0 1'
    '''
    titleInfo='1 1 1'
        
    #线程池最大容量（数字越大，占据内存等资源越多，数字越小，下载越慢，总之看个人电脑状况决定）
    ThreadPoolMaxNum=10
