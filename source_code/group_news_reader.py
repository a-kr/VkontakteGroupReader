# -*- coding: utf-8 -*-
import urllib2
import urllib

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
        wall_posts = GroupWall()

        html = lxml.html.parse( data ).getroot()

        cleaner = Cleaner( style=True, page_structure=False)
        cleaned_html = cleaner.clean_html( html )

        page_wall_posts = cleaned_html.get_element_by_id("page_wall_posts", None)
        if len(page_wall_posts):
            #для каждого поста
            for post_element in page_wall_posts.cssselect(".post.all"):
                #получаем информацию о идентификаторе, авторе, дате создания, содержимом поста
                #и комментариев к нему
                post_id = post_element.attrib["id"].replace('post-','')
                post_table = post_element.cssselect('table.post_table')[0]

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
                wall_posts.add_new_post( post_info )

                replies = post_table.cssselect('div.replies_wrap')[0]

                #поиск кнопки с доп раскрывающимся списком комментов
                has_more_comments = replies.cssselect( 'div.wrh_text' )
                if has_more_comments:
                    print post_id, has_more_comments[0].text_content()
                    additional_request = r'http://vkontakte.ru/al_wall.php?act=get_replies&al=1&count=false&post=-' + post_id
                    print additional_request

                for reply_element in replies.cssselect('div.reply.clear'):
                    reply_id = reply_element.attrib["id"].replace('post-','')
                    reply_table = reply_element.cssselect('table.reply_table')[0]

                    reply_author_img_url = reply_table.cssselect('tr td.image img')[0].attrib['src']
                    reply_author_name = reply_table.cssselect('tr td.info a.author')[0].text_content()
                    reply_author = PostAuthor( reply_author_name, reply_author_img_url )

                    reply_date = reply_table.cssselect('tr td.info a.wd_lnk')[0].text_content()
                    reply_text_elem = reply_table.cssselect('tr td.info div.wall_reply_text')[0]
                    if reply_text_elem.cssselect('span'):
                        reply_text = reply_text_elem.cssselect('span')[1].text_content()
                    else:
                        reply_text = reply_text_elem.text_content()
                    pass

                    comment_info = CommentPostInfo( reply_id, reply_author, reply_date, reply_text )
                    post_info.add_reply( comment_info )
        else:
            raise Exception( 'В HTML нет элемента с id="page_wall_posts"' )
        return wall_posts
