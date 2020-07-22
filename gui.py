#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module originally created by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import AMR_support

from my_randomizer import *

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    AMR_support.set_Tk_var()
    top = TopLevel (root)
    AMR_support.init(root, top)
    root.mainloop()

w = None
def create_TopLevel(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_TopLevel(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    AMR_support.set_Tk_var()
    top = TopLevel (w)
    AMR_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_TopLevel():
    global w
    w.destroy()
    w = None

class TopLevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450")
        top.minsize(120, 1)
        top.maxsize(2564, 1421)
        top.resizable(1, 1)
        top.title("Amazing Mirror Randomizer")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.TFrame1 = ttk.Frame(top)
        self.TFrame1.place(x=20, y=80, height=250, width=560)
        self.TFrame1.configure(relief='groove')
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(relief="groove")

        self.Label_RomInput = ttk.Label(top)
        self.Label_RomInput.place(x=20, y=20,  height=19, width=215)
        self.Label_RomInput.configure(background="#d9d9d9")
        self.Label_RomInput.configure(foreground="#000000")
        self.Label_RomInput.configure(font="TkDefaultFont")
        self.Label_RomInput.configure(relief="flat")
        self.Label_RomInput.configure(anchor='w')
        self.Label_RomInput.configure(justify='left')
        self.Label_RomInput.configure(text='''Kirby & The Amazing Mirror (USA) ROM''')

        self.Button_RomInput = ttk.Button(top)
        self.Button_RomInput.place(x=500, y=18,  height=25, width=76)
        self.Button_RomInput.configure(command=AMR_support.setSourceRom)
        self.Button_RomInput.configure(takefocus="")
        self.Button_RomInput.configure(text='''Select ROM''')

        self.Entry_RomInput = ttk.Entry(top)
        self.Entry_RomInput.place(x=240, y=20, height=21, width=250)
        self.Entry_RomInput.configure(state='readonly')
        self.Entry_RomInput.configure(textvariable=AMR_support.sourceRom)
        self.Entry_RomInput.configure(background="#000000")
        self.Entry_RomInput.configure(cursor="ibeam")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.style.map('TCheckbutton',background=
            [('selected', _bgcolor), ('active', _ana2color)])
        self.CheckButton_RandomizeMiniBosses = ttk.Checkbutton(self.TFrame1)
        self.CheckButton_RandomizeMiniBosses.place(x=20, y=95, width=150
                , height=21)
        self.CheckButton_RandomizeMiniBosses.configure(variable=AMR_support.includeMiniBosses)
        self.CheckButton_RandomizeMiniBosses.configure(offvalue="2")
        self.CheckButton_RandomizeMiniBosses.configure(takefocus="")
        self.CheckButton_RandomizeMiniBosses.configure(text='''Randomize Mini-Bosses''')
        self.tooltip_font = "TkDefaultFont"
        self.CheckButton_RandomizeMiniBosses_tooltip = \
        ToolTip(self.CheckButton_RandomizeMiniBosses, self.tooltip_font, '''Should Mini-Boss abilities also be randomized, or should they stay the same?''')

        self.Label_NumSeeds = ttk.Label(self.TFrame1)
        self.Label_NumSeeds.place(x=400, y=148,  height=21, width=58)
        self.Label_NumSeeds.configure(background="#d9d9d9")
        self.Label_NumSeeds.configure(foreground="#000000")
        self.Label_NumSeeds.configure(font="TkDefaultFont")
        self.Label_NumSeeds.configure(relief="flat")
        self.Label_NumSeeds.configure(anchor='w')
        self.Label_NumSeeds.configure(justify='left')
        self.Label_NumSeeds.configure(text='''# of Seeds''')
        self.tooltip_font = "TkDefaultFont"
        self.Label_NumSeeds_tooltip = \
        ToolTip(self.Label_NumSeeds, self.tooltip_font, '''How many seeds would you like to generate?''')

        self.ComboBox_NumSeeds = ttk.Combobox(self.TFrame1)
        self.ComboBox_NumSeeds.place(x=400, y=170, height=21, width=53)
        self.value_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',]
        self.ComboBox_NumSeeds.configure(values=self.value_list)
        self.ComboBox_NumSeeds.configure(state='readonly')
        self.ComboBox_NumSeeds.configure(textvariable=AMR_support.numSeeds)

        self.style.map('TRadiobutton',background=
            [('selected', _bgcolor), ('active', _ana2color)])
        self.RadioButton_UseSettings = ttk.Radiobutton(top)
        self.RadioButton_UseSettings.place(x=20, y=50, width=89, height=21)
        self.RadioButton_UseSettings.configure(variable=AMR_support.useSeed)
        self.RadioButton_UseSettings.configure(value="2")
        self.RadioButton_UseSettings.configure(text='''Use Settings''')
        self.RadioButton_UseSettings.configure(compound='none')
        self.tooltip_font = "TkDefaultFont"
        self.RadioButton_UseSettings_tooltip = \
        ToolTip(self.RadioButton_UseSettings, self.tooltip_font, '''Use the settings defined below to create a random seed.''')

        self.RadioButton_UseSeed = ttk.Radiobutton(top)
        self.RadioButton_UseSeed.place(x=280, y=50, width=79, height=21)
        self.RadioButton_UseSeed.configure(variable=AMR_support.useSeed)
        self.RadioButton_UseSeed.configure(text='''Use Seed''')
        self.tooltip_font = "TkDefaultFont"
        self.RadioButton_UseSeed_tooltip = \
        ToolTip(self.RadioButton_UseSeed, self.tooltip_font, '''Recreate a specific set of changes according to a 10-character seed.''')

        self.Entry_SeedInput = ttk.Entry(top)
        self.Entry_SeedInput.place(x=360, y=50, height=21, width=130)
        self.Entry_SeedInput.configure(state='disabled')
        self.Entry_SeedInput.configure(textvariable=AMR_support.seedInput)
        self.Entry_SeedInput.configure(takefocus="")
        self.Entry_SeedInput.configure(cursor="ibeam")
        self.Entry_SeedInput.bind('<Key>',AMR_support.keepUpperCharsSeed)
        self.Entry_SeedInput.bind('<KeyRelease>',AMR_support.keepUpperCharsSeed)

        self.CheckButton_GenerateTextLog = ttk.Checkbutton(top)
        self.CheckButton_GenerateTextLog.place(x=150, y=400, width=118
                , height=21)
        self.CheckButton_GenerateTextLog.configure(variable=AMR_support.generateAbilityLog)
        self.CheckButton_GenerateTextLog.configure(takefocus="")
        self.CheckButton_GenerateTextLog.configure(text='''Generate Text Log''')
        self.tooltip_font = "TkDefaultFont"
        self.CheckButton_GenerateTextLog_tooltip = \
        ToolTip(self.CheckButton_GenerateTextLog, self.tooltip_font, '''Would you like to generate a text file that details what abilities are tied to each enemy/object in the created seed?''')

        self.Button_CreateRom = ttk.Button(top)
        self.Button_CreateRom.place(x=330, y=400,  height=25, width=76)
        self.Button_CreateRom.configure(takefocus="")
        self.Button_CreateRom.configure(text='''Randomize!''')

        self.Label_Message = ttk.Label(top)
        self.Label_Message.place(x=30, y=350,  height=30, width=545)
        self.Label_Message.configure(background="#d9d9d9")
        self.Label_Message.configure(foreground="#000000")
        self.Label_Message.configure(font="TkDefaultFont")
        self.Label_Message.configure(relief="flat")
        self.Label_Message.configure(anchor='center')
        self.Label_Message.configure(justify='left')
        self.Label_Message.configure(textvariable=AMR_support.message)

        self.RadioButton_UseSettings.configure(command=self.prepareSettingsAndSeed)
        self.RadioButton_UseSeed.configure(command=self.prepareSettingsAndSeed)
        self.Button_CreateRom.configure(command=self.attemptRandomize)

    def prepareSettingsAndSeed(self, unused=None):
        if AMR_support.useSeed.get()=="1":
            self.Entry_SeedInput.configure(state="normal")
            self.Label_NumSeeds.configure(state="disabled")
            self.ComboBox_NumSeeds.configure(state="disabled")
        else:
            self.Entry_SeedInput.configure(state="disabled")
            self.Label_NumSeeds.configure(state="normal")
            self.ComboBox_NumSeeds.configure(state="readonly")

    def attemptRandomize(self):
        results = randomize()
        AMR_support.message.set(results[1])
        self.Label_Message.configure(foreground="#0000FF" if results[0] else "#FF0000")

# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import time, localtime, strftime

class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.5, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        """
        Updates the Tooltip with a new message. Added by Rozen
        """
        self.msgVar.set(msg)

# ===========================================================
#                   End of Class ToolTip
# ===========================================================

def set_Tk_var():
    global sourceRom
    sourceRom = tk.StringVar()
    global message
    message = tk.StringVar()
    message.set('')
    initVars()

def initVars():
    message.set("Welcome to the Amazing Mirror Randomizer! Move your mouse over a label to learn more about it.")

def setSourceRom():
    global sourceRom
    sourceRom.set(tk.filedialog.askopenfilename(filetypes=[("ROM files", "*."+romFileFormat)]))

def keepUpperCharsSeed(unused):
    global seedInput
    seedInput.set(''.join(ch.upper() for ch in seedInput.get() if ch.isalpha() or ch.isdigit()))
    seedInput.set(seedInput.get()[:10])

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window(endProg=False):
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
    if endProg:
        sys.exit()