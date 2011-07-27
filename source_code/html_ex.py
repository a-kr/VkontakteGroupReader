# coding: utf-8
__author__ = 'Tural'

from lxml.html.clean import Cleaner
import lxml
import os

def func():
    path = os.path.normpath(
        os.path.join(
            os.getcwd(), "..", "vkontakte_group.html" ) )
    f = open( path, "r" )
    html = lxml.html.parse( f ).getroot()

    cleaner = Cleaner( style=True, page_structure=False)
    cleaned_html = cleaner.clean_html( html )

    page_wall_posts = cleaned_html.get_element_by_id("page_wall_posts", None)
    if page_wall_posts:
        for element in page_wall_posts.cssselect(".post.all"):
            post_id = element.attrib["id"].replace('post-','')
            post_table = element.cssselect('table.post_table')[0]
            author_img_url = post_table.cssselect('tr td.image img')[0].attrib['src']
            author_name = post_table.cssselect('tr td.info a.author')[0].text_content()
            post_date = post_table.cssselect('tr td.info span.rel_date')[0].text_content()
            post_text_elem = post_table.cssselect('tr td.info div.wall_post_text')[0]
            post_text = ""
            if post_text_elem.cssselect('span'):
                post_text = post_text_elem.cssselect('span')[1].text_content()
            else:
                post_text = post_text_elem.text_content()

            replies = post_table.cssselect('div.replies_wrap')[0]
            for element in replies.cssselect('div.reply.clear'):
                reply_id = element.attrib["id"].replace('post-','')
                reply_table = element.cssselect('table.reply_table')[0]
                author_img_url = reply_table.cssselect('tr td.image img')[0].attrib['src']
                author_name = reply_table.cssselect('tr td.info a.author')[0].text_content()
                reply_date = reply_table.cssselect('tr td.info a.wd_lnk')[0].text_content()
                reply_text_elem = reply_table.cssselect('tr td.info div.wall_reply_text')[0]
                reply_text = ""
                if reply_text_elem.cssselect('span'):
                    reply_text = reply_text_elem.cssselect('span')[1].text_content()
                else:
                    reply_text = reply_text_elem.text_content()
            #for reply in

                #в таблице post_table
                    #td image
                        #изображение автора
                    #td info
                        #имя автора
                        #текст сообщения
                        #replies
                            #дата поста
                            #replies_wrap
                                #reply_table
                                    #td image
                                        #изображение автора
                                    #td info
                                        #имя автора
                                        #текст сообщения
                                        #дата

if __name__ == '__main__':
    func()