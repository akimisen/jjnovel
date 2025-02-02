#coding=utf-8
import logging, os, re, time
from datetime import datetime
import requests
from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode
from tenacity import retry, stop_after_attempt, wait_fixed
from html2text import html2text
from tasks import tasks_from_newDayList,tasks_from_videoIntro

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                level=logging.INFO)
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
    "Referer": "http://android.jjwxc.net?v=277"
}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_free_chapter(target_nid, target_chapter_id):
    r = requests.get("http://app-cdn.jjwxc.net/androidapi/chapterContent", params={
        "novelId": target_nid,
        "chapterId": target_chapter_id
    }, headers=headers, timeout=5)
    return r.json()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_vip_chapter(target_nid, target_chapter_id, token):
    r = requests.get("http://app.jjwxc.org/androidapi/chapterContent", params={
        "novelId": target_nid,
        "chapterId": target_chapter_id,
        "token": token,
        "versionCode": 206,
        "readState": "readahead"
    }, headers=headers)
    return r.json()

# decrypt token
def des_decrypt(s, token=""):
    en = des("00000000", CBC, "1ae2c94b", pad=None, padmode=PAD_PKCS5)
    #token is required to login
    en.setKey("KK!%G3JdCHJxpAF3%Vg9pN" + token)
    return en.decrypt(b64decode(s)).decode("utf-8")

def des_encrypt(s, token=""):
    en = des("00000000", CBC, "1ae2c94b", pad=None, padmode=PAD_PKCS5)
    en.setKey("KK!%G3JdCHJxpAF3%Vg9pN" + token)
    return b64encode(en.encrypt(s)).decode("utf-8")

def write_file(s, end="\n"):
    with open("output.txt", "a+", encoding="utf-8") as f:
        f.write(s + end)

# if jj_account != "":
#     jj_password = input("请输入晋江密码: ")
#
#     identifiers = ''.join(random.choice("0123456789") for _ in range(18)) + ":null:null"
#
#     login_info = requests.get("https://app.jjwxc.org/androidapi/login", params={
#         "versionCode": 206,
#         "loginName": jj_account,
#         "encode": 1,
#         "loginPassword": des_encrypt(jj_password),
#         "sign": des_encrypt(identifiers),
#         "brand": "Lenovo",
#         "model": "Lenovo",
#         "identifiers": identifiers
#     }, headers=headers).json()
#     if "readerId" in login_info and "token" in login_info:
#         logging.info("账号登录成功: " + str(login_info["readerId"]))
#         login_status = True
#         user_token = login_info['token']
#     else:
#         logging.warning("账号登录失败: " + str(login_info))
# tasks = (t[0] for t in tasks_from_videoIntro())
#task_date = datetime.now().strftime("%Y-%m-%d")
task_date='2023-01-25'
tasks = tasks_from_newDayList(task_date)
t_count=0
for task in tasks:
    nid = task[0]
    rank = task[1]
    title = task[2]
    xx = task[4]
    logging.info(": %s" % nid)
    t_count+=1
    logging.info("Running Task %d, Title:%s..." % (t_count,title))

    # request for basic_info
    basic_info = requests.get("http://app-cdn.jjwxc.net/androidapi/novelbasicinfo", params={
        "novelId": nid
    }, headers=headers).json()
    
    logging.info("Basic Info: %s" % basic_info)
    logging.info("Max ChapterID: %s. VIP ChapterID: %s." % (basic_info['maxChapterId'],basic_info['vipChapterid']))
    logging.info("Loading chapterList...")
    chapter_info = requests.get("http://app-cdn.jjwxc.net/androidapi/chapterList", params={
        "novelId": nid,
        "more": 0,
        "whole": 1
    }, headers=headers).json()

    # novelIntro
    logging.info("Downloading novelIntro...")
    write_file("%s by %s" % (basic_info['novelName'], basic_info['authorName']))
    write_file("\n***文案***")
    logging.info(re.sub(r'(<br/>)+','\n',html2text(basic_info['novelIntro'])))
    write_file(re.sub(r'(<br/>)+','\n',html2text(basic_info['novelIntro'])))
    # write_file("文章类型: " + basic_info['novelClass'])
    # write_file("作品视角: " + basic_info['mainview'])
    # write_file("作品风格: " + basic_info['novelStyle'])
    # write_file("所属系列: " + basic_info['series'])
    # write_file("内容标签: " + basic_info['novelTags'])
    # write_file("一句话简介: " + basic_info['novelIntroShort'])
    # write_file(basic_info['protagonist'] + " " + basic_info['costar'])
    # write_file("评分: " + basic_info['novelReviewScore'] +
    #         " 总积分: " + basic_info['novelScore'] +
    #         " 排名: " + basic_info['ranking'])
    # write_file("")
    # write_file("-----简介-----")
    # write_file(html2text(html2text(basic_info['novelIntro'])))
    
    logging.info("Downloading chapters for novel: %s..." % basic_info['novelName'])
    for i in range(1, int(basic_info['vipChapterid'])):
        if chapter_info['chapterlist'][i-1]['chaptertype'] == "1":
            write_file("### " + chapter_info['chapterlist'][i-1]['chaptername'] + " ###")
            write_file("")
            chapter_info['chapterlist'].pop(i-1)
        
        # chapterName
        # if i>1:
        write_file("----------")
        write_file("第 " + str(i) + " 章  " + chapter_info['chapterlist'][i-1]['chaptername'] + "  " +
                chapter_info['chapterlist'][i-1]['chapterdate'])
        write_file(chapter_info['chapterlist'][i-1]['chaptersize'] + " 字  " +
                chapter_info['chapterlist'][i-1]['chapterintro'])
        write_file("")

        # 处理被锁章节
        if chapter_info['chapterlist'][i-1]['islock'] != '0':
            logging.warning("章节被锁.")
            write_file("章节被锁!")
            write_file("")
            continue

        logging.info("获取章节: " + str(i))
        content = get_free_chapter(nid, i)
        logging.debug(content)

        if "content" in content:
            write_file(html2text(content['content']))
            # if content['sayBody'] != "":
            #     write_file("作者有话说:")
            #     write_file(content['sayBody'])
            #     write_file("")
            logging.info("章节获取成功.")
        else:
            logging.warning("章节获取失败!")
            break

    os.rename('output.txt','file/#%s%s%s_%s.txt' % (rank,xx,task_date.replace('-','')[2:],basic_info['novelName']))
    logging.info("Completed collecting contents for <%s>." % basic_info['novelName'])

    # if not login_status:
    #     logging.warning("未登录, 无法获取V章, 程序结束.")
    #     sys.exit(0)

    # logging.info("尝试获取V章...")

    # for i in range(int(basic_info['vipChapterid']), int(basic_info['maxChapterId']) + 1):
    #     try:
    #         if chapter_info['chapterlist'][i-1]['chaptertype'] == "1":
    #             write_file("### " + chapter_info['chapterlist'][i-1]['chaptername'] + " ###")
    #             write_file("")
    #             chapter_info['chapterlist'].pop(i-1)

    #         write_file("----------")
    #         write_file("第 " + str(i) + " 章  " + chapter_info['chapterlist'][i-1]['chaptername'] + "  " +
    #                 chapter_info['chapterlist'][i-1]['chapterdate'])
    #         write_file(chapter_info['chapterlist'][i-1]['chaptersize'] + " 字  " + chapter_info['chapterlist'][i-1][
    #             'chapterintro'])
    #         write_file("")

    #         # 处理被锁章节
    #         if chapter_info['chapterlist'][i-1]['islock'] != '0':
    #             logging.warning("章节被锁.")
    #             write_file("章节被锁!")
    #             write_file("")
    #             continue

    #         logging.info("获取章节: " + str(i))
    #         content = get_vip_chapter(nid, i, user_token)
    #         logging.debug(content)

    #         if "content" in content:
    #             if "content" in content['encryptField']:
    #                 content['content'] = des_decrypt(content['content'], token=user_token)
    #                 logging.info("解密成功.")
    #                 logging.debug(content['content'])

    #             write_file(html2text(html2text(content['content'])))
    #             if content['sayBody'] != "":
    #                 write_file("作者有话说:")
    #                 write_file(content['sayBody'])
    #                 write_file("")

    #             logging.info("章节获取成功.")
    #         else:
    #             logging.warning("章节获取失败!")

    #         time.sleep(1)
    #     except Exception as e:
    #         write_file("内容获取失败: " + str(e))
    #         logging.exception(e)