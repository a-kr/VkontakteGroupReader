# -*- coding: utf-8 -*-

__author__ = 'Tural'

import urllib
import urllib2
from lxml.html.clean import Cleaner
import lxml

from group_wall_posts import GroupWall
from post import PostAuthor, PostInfo, CommentPostInfo


class VkontakteGroupNewsReader(object):
    def __init__(self, login, password, group_url):
        self.login = login
        self.password = password
        self.group_url = group_url
        self.cookie = self.get_cookie()
        self.current_wall_posts = None

    def get_cookie(self):
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor))
        params = urllib.urlencode({'email': self.login,'pass': self.password})
        request = urllib2.Request('http://vkontakte.ru/login.php', params)
        f = urllib2.urlopen(request)
        cookie = f.headers
        return cookie

    def get_posts(self):
        data = urllib2.urlopen(self.group_url)
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

        cleaner = Cleaner( style=True, page_structure=False)
        cleaned_html = cleaner.clean_html( html )

        page_wall_posts = cleaned_html.get_element_by_id("page_wall_posts", None)
        
        if not page_wall_posts:
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
            post_text = post_text_elem.cssselect('span')[1].text_content()
        else:
            post_text = post_text_elem.text_content()

        post_info = PostInfo( post_id, post_author, post_date, post_text )
        replies = post_table.cssselect('div.replies_wrap')[0]

        #поиск кнопки с доп раскрывающимся списком комментов
        has_more_comments = replies.cssselect( 'div.wrh_text' )
        if has_more_comments:
            post_info.hidden_replies_info = has_more_comments[0].text_content()

        return post_info

    @staticmethod
    def get_reply_from_response_part(reply_html_element):
        reply_id = reply_html_element.attrib["id"].replace('post-','')
        reply_table = reply_html_element.cssselect('table.reply_table')[0]

        reply_author_img_url = reply_table.cssselect('tr td.image img')[0].attrib['src']
        reply_author_name = reply_table.cssselect('tr td.info a.author')[0].text_content()
        reply_author = PostAuthor( reply_author_name, reply_author_img_url )

        reply_date = reply_table.cssselect('tr td.info a.wd_lnk')[0].text_content()
        reply_text_elem = reply_table.cssselect('tr td.info div.wall_reply_text')[0]
        if reply_text_elem.cssselect('span'):
            reply_text = reply_text_elem.cssselect('span')[1].text_content()
        else:
            reply_text = reply_text_elem.text_content()

        comment_info = CommentPostInfo( reply_id, reply_author, reply_date, reply_text )
        return comment_info
        
    def authenticate_with_phone_digits(html_fileobj_with_form):
        """ Нам выдали форму ввода четырех цифр телефона.
            Надо ее заполнить.
            
            html_fileobj_with_form: файлообразный объект, содержащий HTML с формой 
        """
        # crazy code to authenticate ourselves
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