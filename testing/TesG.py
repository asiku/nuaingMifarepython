import wx,os

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="The Main Frame")
        self.SetTopWindow(self.frame)
        self.frame.CenterOnScreen()
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
        pos=wx.DefaultPosition, size=(220,50),
        style=wx.DEFAULT_FRAME_STYLE,
        name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
        pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)

        self.btn1 = wx.Button(self.panel, label="Push Me")
        self.btn2 = wx.Button(self.panel, label="push me too")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.btn1, 0, wx.ALL, 10)
        sizer.Add(self.btn2, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.Bind(wx.EVT_BUTTON,
                  lambda event:
                  self.btn1.Enable(not self.btn1.Enabled),
                  self.btn2)
    def OnButton(self, event):
        """Called when self.btn1 is clicked"""
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        print "Button 1 Clicked:"
        print "ID=%d" % event_id
        print "object=%s" % event_obj.GetLabel()


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()