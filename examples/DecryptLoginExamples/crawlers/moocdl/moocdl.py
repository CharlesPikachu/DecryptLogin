'''
Function:
    MOOC下载器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import time
import click
import random
import shutil
import subprocess
from tqdm import tqdm
from DecryptLogin import login
from urllib.parse import urlencode


'''MOOC下载器'''
class MOOCDL():
    def __init__(self, username='s_sharing@126.com', password='123456', url='https://www.icourse163.org/course/SJTU-1003381021'):
        self.url = url
        self.infos_return, self.session = self.login(username, password)
    '''运行'''
    def run(self):
        url = self.url
        # 从课程主页面获取信息
        url = url.replace('learn/', 'course/')
        response = self.session.get(url)
        term_id = re.findall(r'termId : "(\d+)"', response.text)[0]
        course_name = ' - '.join(re.findall(r'name:"(.+)"', response.text))
        course_name = self.filterBadCharacter(course_name)
        course_id = re.findall(r'https?://www.icourse163.org/(course|learn)/\w+-(\d+)', url)[0]
        self.logging(f'从课程主页面获取的信息如下:\n\t[课程名]: {course_name}, [课程ID]: {course_name}, [TID]: {term_id}')
        # 获取资源列表
        resource_list = []
        data = {
            'tid': term_id,
            'mob-token': self.infos_return['results']['mob-token'],
        }
        response = self.session.post('https://www.icourse163.org/mob/course/courseLearn/v1', data=data)
        course_info = response.json()
        file_types = [1, 3, 4]
        for chapter_num, chapter in enumerate(course_info.get('results', {}).get('termDto', {}).get('chapters', [])):
            for lesson_num, lesson in enumerate(chapter.get('lessons', [])) if chapter.get('lessons') is not None else []:
                for unit_num, unit in enumerate(lesson.get('units', [])):
                    if unit['contentType'] not in file_types: continue
                    savedir = course_name
                    self.checkdir(savedir)
                    for item in [self.filterBadCharacter(chapter['name']), self.filterBadCharacter(lesson['name']), self.filterBadCharacter(unit['name'])]:
                        savedir = os.path.join(savedir, item)
                        self.checkdir(savedir)
                    if unit['contentType'] == file_types[0]:
                        savename = self.filterBadCharacter(unit['name']) + '.mp4'
                        resource_list.append({
                            'savedir': savedir,
                            'savename': savename,
                            'type': 'video',
                            'contentId': unit['contentId'],
                            'id': unit['id'],
                        })
                    elif unit['contentType'] == file_types[1]:
                        savename = self.filterBadCharacter(unit['name']) + '.pdf'
                        resource_list.append({
                            'savedir': savedir,
                            'savename': savename,
                            'type': 'pdf',
                            'contentId': unit['contentId'],
                            'id': unit['id'],
                        })
                    elif unit['contentType'] == file_types[2]:
                        if unit.get('jsonContent'):
                            json_content = eval(unit['jsonContent'])
                            savename = self.filterBadCharacter(json_content['fileName'])
                            resource_list.append({
                                'savedir': savedir,
                                'savename': savename,
                                'type': 'rich_text',
                                'jsonContent': json_content,
                            })
        self.logging(f'成功获得资源列表, 数量为{len(resource_list)}')
        # 下载对应资源
        pbar = tqdm(resource_list)
        for resource in pbar:
            pbar.set_description(f'downloading {resource["savename"]}')
            # --下载视频
            if resource['type'] == 'video':
                data = {
                    'bizType': '1',
                    'mob-token': self.infos_return['results']['mob-token'],
                    'bizId': resource['id'],
                    'contentType': '1',
                }
                while True:
                    response = self.session.post('https://www.icourse163.org/mob/j/v1/mobileResourceRpcBean.getResourceToken.rpc', data=data)
                    if response.json()['results'] is not None: break
                    time.sleep(0.5 + random.random())
                signature = response.json()['results']['videoSignDto']['signature']
                data = {
                    'enVersion': '1',
                    'clientType': '2',
                    'mob-token': self.infos_return['results']['mob-token'],
                    'signature': signature,
                    'videoId': resource['contentId'],
                }
                response = self.session.post('https://vod.study.163.com/mob/api/v1/vod/videoByNative', data=data)
                # ----下载视频
                videos = response.json()['results']['videoInfo']['videos']
                resolutions, video_url = [3, 2, 1], None
                for resolution in resolutions:
                    for video in videos:
                        if video['quality'] == resolution:
                            video_url = video["videoUrl"]
                            break
                    if video_url is not None: break
                if '.m3u8' in video_url:
                    self.m3u8download({
                        'download_url': video_url,
                        'savedir': resource['savedir'],
                        'savename': resource['savename'],
                    })
                else:
                    self.defaultdownload({
                        'download_url': video_url,
                        'savedir': resource['savedir'],
                        'savename': resource['savename'],
                    })
                # ----下载字幕
                srt_info = response.json()['results']['videoInfo']['srtCaptions']
                if srt_info:
                    for srt_item in srt_info:
                        srt_name = os.path.splitext(resource['savename'])[0] + '_' + srt_item['languageCode'] + '.srt'
                        srt_url = srt_item['url']
                        response = self.session.get(srt_url)
                        fp = open(os.path.join(resource['savedir'], srt_name), 'wb')
                        fp.write(response.content)
                        fp.close()
            # --下载PDF
            elif resource['type'] == 'pdf':
                data = {
                    't': '3',
                    'cid': resource['contentId'],
                    'unitId': resource['id'],
                    'mob-token': self.infos_return['results']['mob-token'],
                }
                response = self.session.post('http://www.icourse163.org/mob/course/learn/v1', data=data)
                pdf_url = response.json()['results']['learnInfo']['textOrigUrl']
                self.defaultdownload({
                    'download_url': pdf_url,
                    'savedir': resource['savedir'],
                    'savename': resource['savename'],
                })
            # --下载富文本
            elif resource['type'] == 'rich_text':
                download_url = 'http://www.icourse163.org/mob/course/attachment.htm?' + urlencode(resource['jsonContent'])
                self.defaultdownload({
                    'download_url': download_url,
                    'savedir': resource['savedir'],
                    'savename': resource['savename'],
                })
    '''登录'''
    def login(self, username, password):
        lg = login.Login()
        infos_return, session = lg.icourse163(username, password)
        return infos_return, session
    '''检查文件夹是否存在'''
    def checkdir(self, dirpath):
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
            return False
        return True
    '''清除可能出问题的字符'''
    def filterBadCharacter(self, string):
        need_removed_strs = ['<em>', '</em>', '<', '>', '\\', '/', '?', ':', '"', '：', '|', '？', '*']
        for item in need_removed_strs:
            string = string.replace(item, '')
        try:
            rule = re.compile(u'[\U00010000-\U0010ffff]')
        except:
            rule = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        string = rule.sub('', string)
        return string.strip().encode('utf-8', 'ignore').decode('utf-8')
    '''默认下载器'''
    def defaultdownload(self, info):
        try:
            is_success = False
            with self.session.get(info['download_url'], stream=True, verify=False) as response:
                if response.status_code == 200:
                    total_size, chunk_size = int(response.headers['content-length']), 1024
                    label = '[FileSize]: %0.2fMB' % (total_size / 1024 / 1024)
                    with click.progressbar(length=total_size, label=label) as progressbar:
                        with open(os.path.join(info['savedir'], info['savename']), 'wb') as fp:
                            for chunk in response.iter_content(chunk_size=chunk_size):
                                if chunk:
                                    fp.write(chunk)
                                    progressbar.update(len(chunk))
                    is_success = True
        except:
            is_success = False
        return is_success
    '''下载m3u8文件'''
    def m3u8download(self, info):
        savepath = os.path.join(info['savedir'], info['savename'])
        ext = os.path.splitext(info['savename'])[-1]
        download_url = info['download_url']
        p = subprocess.Popen(f'ffmpeg -i "{download_url}" tmp.{ext}')
        while True:
            if subprocess.Popen.poll(p) is not None: 
                shutil.move(f'tmp.{ext}', savepath)
                return True
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')