# -*- coding: GBK -*-
import tkinter as tk
import os, json,subprocess,threading
from tkinter import filedialog,messagebox

from mymodule.customNotebook import *
from mymodule.printv import *
'''
容易卡崩,电脑重启后恢复正常
选项卡关闭提醒未完善
Easy to crash, restart the computer to restore normal TAB closed reminder is not perfect
'''
xy = [70,70]
with open(r"D:\pycode\configuration.json",mode='r') as sfile:
    setting = json.loads(sfile.read())
    cl = setting["cl"]
class Textw(object):
    def __init__(self,a,num):
        self.rfn = ''
        self.openmodel = 'r+'
        self.filepath = a[1]
        self.filetype = None
        self.hasfile = False
        self.filename = 'Untitled-{0}'.format(num)
        self.filetext = ''
        self.filec = ''
        self.compiler = None
    def r(self,mtkw):
        return tk.Text(mtkw)
class Tkw(object):
    def __init__(self,a):
        self.tfilepath = None
        self.windowList = []
        self.windowNumber = 0
        self.tkw = tk.Tk()
        self.username = setting["username"]
        self.tkw.title(self.username)
        self.tkw.geometry('1200x640+%d+%d'%(a[0][0],a[0][1]))
        self.tkw.iconbitmap('D:\pycode\image\pycode.ico')
        #fontsetting
        self.enb = CustomNotebook(self.cangefunc,self.closefunc,self.tkw)
        self.enb.pack(side='top',fill='both',expand=True)
        self.enb.enable_traversal()
        self.start = tk.Label(self.tkw,text='大煤气',bg='red')
        self.enb.add(self.start,text='hi')
        self.enb.enable_traversal()
        # self.frame1 = tk.Frame(self.tkw,bg='red')
        # self.frame1.pack(side='left',fill='x',expand=True)
        self.console = tk.Text(self.tkw,undo=True,yscrollcommand=True)
        self.console.pack(side='bottom',fill='x',)
        self.sm = True

        self.topmenu = tk.Menu(self.tkw)
        self.filemenu = tk.Menu(self.topmenu,tearoff=False)
        self.filemenu.add_command(label='新建 Ctrl+N',command = self.openNewWindow)
        self.tkw.bind('<Control-n>',self.openNewWindow)
        self.filemenu.add_command(label='打开 Ctrl+O',command = self.fileopen)
        self.tkw.bind('<Control-o>',self.fileopen)
        self.filemenu.add_command(label='保存 Ctrl+S',command = self.filesave)
        self.tkw.bind('<Control-n>',self.filesave)
        self.topmenu.add_cascade(label='文件(F)',menu=self.filemenu)
        self.topmenu.add_command(label='配置(|)',command=self.ccange)
        self.tkw.bind('<Control-1>',self.ccange)
        self.topmenu.add_command(label='解释(I)',command=self.irun)
        self.tkw.bind('<Control-i>',self.irun)
        self.tkw.bind('<F5>',self.irun)
        self.topmenu.add_command(label='编译(C)',command=self.crun)
        self.tkw.bind('<Control-Alt-c>',self.crun)
        self.topmenu.add_command(label='运行(R)',command=self.run)
        self.tkw.bind('<Control-Alt-r>',self.run)
        self.tkw.config(menu=self.topmenu)
        self.tkw.mainloop()
    def fileopen(self,n=None,):
        self.tfilepath = filedialog.askopenfilename()
        self.windowNumber += 1
        exec('wlt = Textw([xy,"{}"],{})'.format(self.tfilepath,self.windowNumber))
        exec('wl%d = [wlt.r(self.tkw),wlt];self.windowList.append(wl%d)'%(self.windowNumber,self.windowNumber))
        tq = self.windowList[-1]
        with open(self.tfilepath,mode=tq[1].openmodel) as file:
            self.tfiletype = self.getFile(self.tfilepath)
            filecode = file.read()
            tq[1].filetext = filecode
            tq[0].insert('insert',filecode)
            tq[1].filetype = self.tfiletype[0][1]
            tq[1].filepath = self.tfilepath
            tq[1].filename = self.tfiletype[1]
            tq[1].filec = self.tfiletype[0][0]
            tq[1].rfn = tq[1].filec + '.exe'
            tq[1].compiler = setting[cl[tq[1].filetype]]
            tq[1].hasfile = True
            self.enb.add(tq[0],text=tq[1].filename,image=setting["image"][self.getFile(self.tfilepath)[0][1]])
            self.tkw.title('{0}-{1}'.format(self.windowList[self.windowNumber-1][1].filename,self.username))
        if self.sm == True:
            self.enb.forget(0)
            self.sm = False
        if len(self.windowList) == 8:
            n = messagebox.askokcancel('warring info','当前打开文件较多,建议新建窗口\nYou are advised to create a new window because there are many open files\a')
            if n == True:
                os.system('python %s'%(setting["path"]))
        return
    def filesave(self,m=True):
        self.tnowfile = self.windowList[int(self.enb.select()[-1])-2]
        self.tnowfile[1].filetext = self.tnowfile[0].get(1.0,"end")
        if self.tnowfile[1].hasfile == False:
            wfile = filedialog.asksaveasfile()
            wfile.write(self.windowList[self.tnowfile[1]].filetext)
            wfile.close()
        else:
            with open(self.tnowfile[1].filepath,mode="r+") as file:
                file.write(self.tnowfile[1].filetext)
        if m == True:
            messagebox.showinfo('save info','保存成功\nsave successfully')
    def irun(self):
        command,commr = '',''
        self.filesave(m=False)
        self.tnowfile = self.windowList[int(self.enb.select()[-1])-2]
        self.tfiletype = self.tnowfile[1].filetype
        self.tfilepath = self.tnowfile[1].filepath
        compiler = self.tnowfile[1].compiler
        if compiler["interpretationTemplate"] == None:
            messagebox.showwarning('warning info','此语言无法解释\nThis language cannot be explained\a')
            return
        else:
            command = compiler["interpretationTemplate"]
            self.consolec = subprocess.run(command.format(file = self.tfilepath),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,shell=True)
            self.console.insert('end','\n%s'%(self.consolec.stdout))
            # self.consolec.stdout.close()
    def crun(self):
        command,commr = '',''
        self.filesave(m=False)
        self.tnowfile = self.windowList[int(self.enb.select()[-1])-2]
        self.tfiletype = self.tnowfile[1].filetype
        self.tfilepath = self.tnowfile[1].filepath
        compiler = self.tnowfile[1].compiler
        if compiler["compileTemplate"] == None:
            messagebox.showwarning('warning info','此语言无法编译\nThis language cannot be explained\a')
            return
        else:
            command = compiler["compileTemplate"]
            self.consolec = subprocess.run(command.format(file=self.tfilepath,modulepath=r"mymodule\pycode_compile.py",filenameNoExtension=self.tnowfile[1].filec),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,shell=True)
            self.console.insert('end','\n%s'%(self.consolec.stdout))
            # self.consolec.stdout.close()
    def run(self):
        self.filesave(m=False)
        self.tnowfile = self.windowList[int(self.enb.select()[-1])-2]
        if self.tnowfile[1].filetype == '.py':
            self.irun()
        else:
            self.consolec = subprocess.run(self.tnowfile[1].rfn,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,shell=True)
            self.console.insert('end','\n%s'%(self.consolec.stdout))
    def ccange(self):
        pass
    def getFile(self,fpath):
        path=fpath
        ftype=os.path.splitext(path)
        fanme = os.path.basename(fpath)
        return [ftype,fanme]
    def openNewWindow(self):
        self.windowNumber += 1
        print(self.windowNumber)
        self.wl = ''
        exec(printv('self.wl'+str(self.windowNumber),' = [Textw([[xy],"',self.windowNumber,'"],',self.tfilepath,').r(self.tkw),Textw([[xy],"',self.windowNumber,'"],',self.tfilepath,')];self.windowList.append(self.wl',self.wl,')',sep='',end=''))
        self.frame2.add(self.windowList[self.windowNumber-1][0],text=self.windowList[self.windowNumber-1][1].filename)
    def cangefunc():
        pass    
    def closefunc():
        pass
tkw1 = Tkw([xy,None])