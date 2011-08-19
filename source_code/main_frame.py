#coding: utf-8
__author__ = 'Tural'

import sys, wx
from group_news_reader import VkontakteGroupNewsReader
from topic_panel import TopicPanel
import login
import urllib2
from lxml.html.clean import Cleaner
import lxml
from post import PostAuthor, CommentPostInfo

class StatusTaskBarIcon(wx.TaskBarIcon):
    """меню в системном трее"""
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = parent
        self.noNewPostsIcon = wx.Icon("tray_icon.png",wx.BITMAP_TYPE_PNG)
        self.newPostsIcon = wx.Icon("tray_icon.png",wx.BITMAP_TYPE_PNG)
        self.CreateMenu()
        self.SetIconImage()

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)

        self.menu=wx.Menu()
        self.menu.Append(wx.ID_REFRESH, u"Обновить")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, u"Выход")

    def ShowMenu(self,event):
        self.PopupMenu(self.menu)

    def SetIconImage(self, is_new_post=False):
        if is_new_post:
            self.SetIcon(self.newPostsIcon, u"Есть новые посты")
        else:
            self.SetIcon(self.noNewPostsIcon, u"Нет новых постов")

def create(parent):
    return WallPostsFrame(parent)

class WallPostsFrame(wx.Frame):
    def _init_sizers(self):
        # generated method, don't edit
        self.bsSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.scrolledWindow1.SetSizerAndFit(self.bsSizer)

    """основное окно программы"""
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wx.NewId(), name=u'GroupNewsReader',
            title=u'VkontakteGroupReader', parent=prnt, pos=wx.Point(516, 141), size=wx.Size(290, 400),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.Center(wx.BOTH)
        self.SetBackgroundColour('#FFFFFF')

        self.scrolledWindow1 = wx.ScrolledWindow(id=wx.ID_ANY,
              name='scrolledWindow1', parent=self, pos=wx.Point(0, 0),
              style=wx.VSCROLL)
        self.scrolledWindow1.SetScrollRate( 0, 1 )

        self.tbicon = StatusTaskBarIcon(self)
        self.tbicon.Bind(wx.EVT_MENU, self.exitApp, id=wx.ID_EXIT)
        self.tbicon.Bind(wx.EVT_MENU, self.refresh_posts, id=wx.ID_REFRESH )

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh_posts, self.timer)
        self.timer.Start(2 * 60 * 1000)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.vk = VkontakteGroupNewsReader(login.login, login.password, login.group_url)
        self.refresh_posts()

    def draw_topics(self):
        self.bsSizer.Clear(True)
        for post_id, post in self.vk.current_wall_posts.posts.iteritems():
            tp = TopicPanel(self.scrolledWindow1, "post_" + post_id, False, post_id, post.author.name, post.date,
                post.text, post.author.image_url, None, post.is_new)
            self.bsSizer.Add(tp, flag=wx.ALIGN_LEFT)

            #кнопка с дополнительными комментами, если такая имеется
            if post.hide_replies_info is not None:
                btnShowHiden = wx.Button(id=wx.ID_ANY, label=post.hide_replies_info,
                    name="btn_" + post_id, parent=self.scrolledWindow1, style=0)
                btnShowHiden.Bind(wx.EVT_BUTTON, self.OnShowHidenButton, id=btnShowHiden.Id)
                self.bsSizer.Add( btnShowHiden )

            for reply_id, reply in post.replies.iteritems():
                tp_r = TopicPanel(self.scrolledWindow1, "reply_" + reply_id, True, reply_id, reply.author.name, reply.date,
                    reply.text, reply.author.image_url, post_id, reply.is_new)
                self.bsSizer.Add(tp_r, flag=wx.LEFT, border=10)
        self.scrolledWindow1.Layout()

    def OnShowHidenButton(self, event):
        post_id = event.EventObject.Name.replace('btn_', '')
        post = self.vk.current_wall_posts.posts[post_id]
        data = urllib2.urlopen(post.get_hide_comments_url())
        html = lxml.html.parse( data ).getroot()

        cleaner = Cleaner( style=True, page_structure=False)
        cleaned_html = cleaner.clean_html( html )

        hiden_comments = list()
        for reply_element in cleaned_html.cssselect('div.reply.clear'):
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

            comment_info = CommentPostInfo( reply_id, reply_author, reply_date, reply_text )
            hiden_comments.append( comment_info )
        post.prepend_list_of_replies( hiden_comments )
        post.hide_replies_info = None
        self.draw_topics()

    def refresh_posts(self, event=None):
        self.vk.get_posts()
        self.draw_topics()

    def exitApp(self,event):
        self.timer.Stop()
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        sys.exit()
