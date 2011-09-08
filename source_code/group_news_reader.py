# -*- coding: utf-8 -*-

__author__ = 'Tural'

import urlparse
import urllib
import urllib2
from lxml.html.clean import Cleaner
import lxml

from cStringIO import StringIO

import codecs
import re

from group_wall_posts import GroupWall
from post import PostAuthor, PostInfo, CommentPostInfo


class VkontakteGroupNewsReader(object):
    def __init__(self, login, password, group_url):
        self.login = login
        self.password = password
        self.group_url = group_url
        self.do_login()
        self.current_wall_posts = None
        
    def do_login(self):
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor))
        params = urllib.urlencode({'email': self.login,'pass': self.password})
        request = urllib2.Request('http://vkontakte.ru/login.php', params)
        f = urllib2.urlopen(request)
        cookie = f.headers

    def get_posts(self):
        response = urllib2.urlopen(self.group_url)
        data = StringIO(response.read())
        wall = self.parse_response( data )
        if self.current_wall_posts:
            if wall.check_for_new_posts_and_comments( self.current_wall_posts ):
                self.current_wall_posts = wall
                print 'something new'
            else:
                print 'nothing new'
        else:
            self.current_wall_posts = wall
            print 'first load'

    @staticmethod
    def parse_response(data):
        """ Возвращает экземпляр GroupWall, или None, если стену распарсить
            по каким-либо причинам не получается. 
        """
        wall_posts = GroupWall()
        html = lxml.html.parse( data ).getroot()

        #cleaner = Cleaner( style=True, page_structure=False)
        cleaned_html = html # cleaner.clean_html( html )

        page_wall_posts = cleaned_html.get_element_by_id("page_wall_posts", None)
        
        if page_wall_posts is None:
            data.seek(0)
            VkontakteGroupNewsReader.authenticate_with_phone_digits(data)
            return None
            
        #для каждого поста
        for post_element in page_wall_posts.cssselect(".post.all"):
            #получаем информацию о идентификаторе, авторе, дате создания, содержимом поста
            #и комментариев к нему
            post_info = VkontakteGroupNewsReader.get_post_from_response_part( post_element )
            wall_posts.add_new_post( post_info )
            post_table = post_element.cssselect('table.post_table')[0]
            replies = post_table.cssselect('div.replies_wrap')[0]
            
            # прикрепленные изображения
            media = post_table.cssselect('a.photo')
            for link in media:
                thumb_img = link.cssselect('img')[0]
                thumb_url = thumb_img.attrib['src']
                #import pdb; pdb.set_trace()
                big_url_script = link.attrib['onclick']
                big_url = re.findall('x_src\: "([^"]+)"', big_url_script)[0]
                print thumb_url, big_url
                post_info.images.append((thumb_url, big_url))
            
            # прикрепленные ссылки
            links = post_table.cssselect('a.lnk')
            for link in links:
                url = link.attrib['href']
                if 'away.php?' in url:
                    url = urlparse.parse_qs(url)
                    url = (url.get('/away.php?to', None) or url.get('http://vkontakte.ru/away.php?to', None) or ['dunno'])[0]
                post_info.links.append(url)
            
            for reply_element in replies.cssselect('div.reply.clear'):
                post_info.add_reply( VkontakteGroupNewsReader.get_reply_from_response_part( reply_element ) )
        return wall_posts

    @staticmethod
    def get_post_from_response_part(post_html_element):
        #получаем информацию о идентификаторе, авторе, дате создания, содержимом поста
        #и комментариев к нему
        post_id = post_html_element.attrib["id"].replace('post-','')
        post_table = post_html_element.cssselect('table.post_table')[0]

        post_author_img_url = post_table.cssselect('tr td.image img')[0].attrib['src']
        post_author_name = post_table.cssselect('tr td.info a.author')[0].text_content()
        post_author = PostAuthor( post_author_name, post_author_img_url )

        post_date = post_table.cssselect('tr td.info span.rel_date')[0].text_content()
        post_text_elem = post_table.cssselect('tr td.info div.wall_post_text')[0]
        if post_text_elem.cssselect('span'):
            post_text_elem = post_text_elem.cssselect('span')[1]
        post_text_lines = []
        for line in post_text_elem.itertext():
            post_text_lines.append(line)
        post_text = '\n'.join(post_text_lines)
        
        post_info = PostInfo( post_id, post_author, post_date, post_text )
        replies = post_table.cssselect('div.replies_wrap')[0]

        #поиск кнопки с доп раскрывающимся списком комментов
        has_more_comments = replies.cssselect( 'div.wrh_text' )
        if has_more_comments:
            post_info.hidden_replies_info = has_more_comments[0].text_content()

        return post_info

    @staticmethod
    def get_reply_from_response_part(reply_html_element):
        """ Возвращает CommentPostInfo """
        reply_id = reply_html_element.attrib["id"].replace('post-','')
        reply_table = reply_html_element.cssselect('table.reply_table')[0]

        reply_author_img_url = reply_table.cssselect('tr td.image img')[0].attrib['src']
        reply_author_name = reply_table.cssselect('tr td.info a.author')[0].text_content()
        reply_author = PostAuthor( reply_author_name, reply_author_img_url )

        reply_date = reply_table.cssselect('tr td.info a.wd_lnk')[0].text_content()
        reply_text_elem = reply_table.cssselect('tr td.info div.wall_reply_text')[0]
        if reply_text_elem.cssselect('span'):
            reply_text_elem = reply_text_elem.cssselect('span')[1]
            
        reply_text_lines = []
        for line in reply_text_elem.itertext():
            reply_text_lines.append(line)
        reply_text = '\n'.join(reply_text_lines)

        comment_info = CommentPostInfo( reply_id, reply_author, reply_date, reply_text )
        return comment_info
        
    @staticmethod
    def get_hidden_comments(hidden_comments_url):
        """ Загружает скрытые комментарии и возвращает список объектов CommentPostInfo """
        data = urllib2.urlopen(hidden_comments_url).read().decode('cp1251')
        #возвращает элемент, а не дерево
        html = lxml.html.document_fromstring( data )
        cleaner = Cleaner( style=True, page_structure=False )
        cleaned_html = cleaner.clean_html( html )
        hidden_comments = list()
        for reply_element in cleaned_html.cssselect('div.reply.clear'):
            hidden_comments.append( VkontakteGroupNewsReader.get_reply_from_response_part( reply_element ) )
        return hidden_comments
        
    @staticmethod
    def authenticate_with_phone_digits(html_fileobj_with_form):
        """ Нам выдали форму ввода четырех цифр телефона.
            Надо ее заполнить.
            
            html_fileobj_with_form: файлообразный объект, содержащий HTML с формой 
        """
        f = open('vk.html', 'w')
        f.write(html_fileobj_with_form.read())
        f.close()
        # crazy code to authenticate ourselves
        import login
        params = urllib.urlencode({
            'act': 'security_check', 
            'al': 1,
            'al_page': '',
            'code': login.phone_digits,
            'hash': '9605d0ffbaa08c8778', # TODO: по-хорошему его надо извлечь из страницы
        })
        request = urllib2.Request('http://vkontakte.ru/login.php')
        # накидаем хедеров для пущей важности...
        request.add_header("Content-type", "application/x-www-form-urlencoded")
        request.add_header("Accept", "*/*")
        request.add_header("Accept-Charset", "windows-1251,utf-8;q=0.7,*;q=0.3")
        request.add_header("Accept-Encoding", "gzip,deflate,sdch")
        request.add_header("Accept-Language", "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4")
        request.add_header("Origin", "http://vkontakte.ru")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1")
        request.add_header("X-Requested-With", "XMLHttpRequest")
        
        f = urllib2.urlopen(request, data=params)