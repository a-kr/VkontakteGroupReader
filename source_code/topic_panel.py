#coding: utf-8
__author__ = 'Tural'

import wx

class TopicPanel( wx.Panel ):
    """панель для отображения топиков и комментариев к ним. Одна панель - один топик"""
    def __init__(self, p_parent, p_name, is_comment, id, author, date, text,
                 image_url, topic_parent=None, is_new=False):
        if is_comment:
            p_size = wx.Size( 250, 130 )
        else:
            p_size = wx.Size( 260, 130 )

        if is_new:
            self.BackgroundColour = wx.Color('yellow')

        wx.Panel.__init__( self, id = wx.NewId(), name = p_name, parent = p_parent, style = wx.BORDER_DOUBLE)
        self.topic_parent = topic_parent

        self.stAuthor = wx.StaticText(id=wx.NewId(),
              label=author,
              name='st_author_' + id, parent=self, pos=wx.Point(60, 5), size=wx.Size(70, 13), style=0)
        self.stAuthor.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))


        self.stText = wx.StaticText(id=wx.NewId(),
              label=text,
              name='st_text_' + id, parent=self, pos=wx.Point(40, 20),
              size=wx.Size(170, 90), style=wx.ST_NO_AUTORESIZE)
        self.stText.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        self.stDate = wx.StaticText(id=wx.NewId(),
              label=date,
              name='st_date_' + id, parent=self, pos=wx.Point(160, 110), size=wx.Size(70, 13), style=0)
        self.stDate.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        #чтобы сайзер не раздувал панели на максимальную ширину и не уменишал меньше
        #заданного размера
        self.SetMinSize(p_size)
        self.SetMaxSize(p_size)

  