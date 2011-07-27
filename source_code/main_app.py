#coding: utf-8
#Boa:App:BoaApp

__author__ = 'Tural'

import main_frame
import wx

class BoaApp(wx.App):
    def OnInit(self):
        self.main = main_frame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
  