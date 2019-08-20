import time
import win32gui
import wx

class TrackerGUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(TrackerGUI, self).__init__(*args, **kw)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Get started by pressing the Start Tracking button!")
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)               
        self.btn = wx.Button(panel, label='Start Tracking')
        self.btn.Bind(wx.EVT_BUTTON, self.OnButtonPress)
        my_sizer.Add(self.btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)
        self.processes = {}
    
    def trackStart(self, window):
        """Updates the dictionary with duration of parameter window's activity"""
        print("TRACKING START")
        nextWindow = str(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        while(nextWindow == window):
            if window in self.processes.keys():
                self.processes.update({window : self.processes.get(window) + 1})
            else:
                self.processes.update({window : 0})
            time.sleep(1)
            nextWindow = str(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        print("Finished Window!")
        return nextWindow
        
    def printDict(self, processDict):
        """DEBUG FUNCTION"""
        if(len(processDict.keys()) != 0):
            for i in processDict.keys():
                print("Key: " + str(i) + " Value: " + str(processDict.get(i)))

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        welcomeItem = fileMenu.Append(-1, "&Welcome\tCtrl-H", "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnWelcome, welcomeItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.printDict(self.processes)
        #print("EXIT")
        self.Close(True)



    def OnWelcome(self, event):
        """Say hello to the user."""
        wx.MessageBox("Start tracking my progress!")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Created by Max Kunz (2019) \n This application tracks the window currently open and creates time elapsed data",
                      "Help",
                      wx.OK|wx.ICON_INFORMATION)


    def OnButtonPress(self, event):
        self.Hide()
        count = 0
        while(count < 10):
            nextWindow = self.trackStart(str(win32gui.GetWindowText(win32gui.GetForegroundWindow())))
            self.printDict(self.processes)
            count += 1
        self.Show()    

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = TrackerGUI(None, title='Time Tracker')
    frm.Show()
    app.MainLoop()
