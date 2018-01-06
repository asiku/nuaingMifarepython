import wx, os,subprocess

cwd = os.getcwd()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Service Presensi")
        self.SetTopWindow(self.frame)
        self.frame.CenterOnScreen()
        self.frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=(220, 80),
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)

        self.btn1 = wx.Button(self.panel, label="Star server")
        self.btn2 = wx.Button(self.panel, label="Stop server")
        self.txt=wx.StaticText(self.panel,label="",style=wx.ALIGN_CENTRE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        gsizer=wx.GridSizer(1,2,0,0)

        gsizer.Add(self.btn1, 0,wx.ALL,8)
        gsizer.Add(self.btn2, 0,wx.ALL,8    )

        sizer.Add(self.txt,0, wx.ALL , 10)
        sizer.Add(gsizer,wx.ALL)
        self.panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.Bind(wx.EVT_BUTTON,self.OnStop,self.btn2)


    def OnButton(self, event):
        try:
            p = subprocess.Popen("python " + cwd + "/tesFlask.py", stdout=subprocess.PIPE, shell=True)
            # self.txt.SetLabel(p.communicate()[0])
            self.txt.SetLabel("Start Server ......")
        except subprocess.CalledProcessError as e:
            self.txt.SetLabel("Ada Error: "+e.output)
            # print e.output


    def OnStop(self,event):
        try:
            p = subprocess.Popen("python " + cwd + "/ShutD.py", stdout=subprocess.PIPE, shell=True)
            self.txt.SetLabel("Stop Server ......")
        except subprocess.CalledProcessError as e:
            self.txt.SetLabel("Ada Error: "+e.output)
            # print e.output

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()