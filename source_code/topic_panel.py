#coding: utf-8
import cStringIO

__author__ = 'Tural'

import wx
import urllib2

class TopicPanel( wx.Panel ):
    """панель для отображения топиков и комментариев к ним. Одна панель - один топик"""
    def __init__(self, p_parent, p_name, is_comment, id, author, date, text,
                 image_url, topic_parent=None, is_new=False):
        if is_comment:
            p_size = wx.Size( 250, -1 )
        else:
            p_size = wx.Size( 260, -1 )

        wx.Panel.__init__( self, id = wx.NewId(), name = p_name, parent = p_parent,
                           style=wx.SUNKEN_BORDER)
        self.topic_parent = topic_parent

        if is_comment:
            self.SetBackgroundColour('#FFFFFF')
        else:
            self.SetBackgroundColour('#B9D3EE')
        if is_new:
            self.SetBackgroundColour('#FFAEB9')

        imgstream = urllib2.urlopen(image_url).read()
        stream=cStringIO.StringIO(imgstream)

        try:
            bmp = wx.BitmapFromImage( wx.ImageFromStream(stream) )
            wx.StaticBitmap(self, wx.ID_ANY, bmp, pos=wx.Point(5,5))
        except Exception as e:
            print e.message

        self.stAuthor = wx.StaticText(id=wx.NewId(),
              label=author,
              name='st_author_' + id, parent=self, pos=wx.Point(60, 5), size=wx.Size(70, 13), style=0)
        self.stAuthor.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))

        self.stText = wx.StaticText(id=wx.NewId(),
              label=text,
              name='st_text_' + id, parent=self, pos=wx.Point(60, 20),
              style=wx.ST_NO_AUTORESIZE)
        self.stText.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        new_width = 170
        width, height = self.stText.GetBestSizeTuple()
        new_height = (width / new_width + 2) * 13
        self.stText.SetSize( wx.Size(new_width, new_height) )


        self.stDate = wx.StaticText(id=wx.NewId(),
              label=date,
              name='st_date_' + id, parent=self, pos=wx.Point(160, 40 + new_height),
              size=wx.Size(70, 13), style=0)
        self.stDate.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        #чтобы сайзер не раздувал панели на максимальную ширину и не уменишал меньше
        #заданного размера
        self.SetMinSize(p_size)
        self.SetMaxSize(p_size)

  