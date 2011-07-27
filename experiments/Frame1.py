#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1SCROLLEDWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(2)]

[wxID_FRAME1TIMER1] = [wx.NewId() for _init_utils in range(1)]

class Frame1(wx.Frame):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_FRAME1TIMER1, owner=self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1Timer, id=wxID_FRAME1TIMER1)
        
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(323, 138), size=wx.Size(241, 360),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self._init_utils()
        self.SetClientSize(wx.Size(233, 326))

        self.scrolledWindow1 = wx.ScrolledWindow(id=wxID_FRAME1SCROLLEDWINDOW1,
              name='scrolledWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(233, 326), style=wx.VSCROLL)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.timer1.Start(200)

    def OnTimer1Timer(self, event):
        wx.MessageDialog('asdf')
