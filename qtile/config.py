# -*- coding: utf-8 -*-
#Customized config.py file written by Martijn van Zuilen. Based upon the default config. Please respect the license written below:
#
# The following comments are the copyright and licensing information from the default
# qtile config. Copyright (c) 2010 Aldo Cortesi, 2010, 2014 dequis, 2012 Randall Ma,
# 2012-2014 Tycho Andersen, 2012 Craig Barnes, 2013 horsik, 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

##### IMPORTS #####

import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer

##### DEFINING SOME WINDOW FUNCTIONS #####

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

##### LAUNCH APPS IN SPECIFIED GROUPS #####

def app_or_group(group, app):
    def f(qtile):
        if qtile.groupMap[group].windows:
            qtile.groupMap[group].cmd_toscreen()
        else:
            qtile.groupMap[group].cmd_toscreen()
            qtile.cmd_spawn(app)
    return f

##### KEYBINDINGS #####

def init_keys():
    keys = [
            Key(
                [mod], "Return",
                lazy.spawn(myTerm)                      # Open terminal
                ),
            Key(
                [mod], "Tab",
                lazy.next_layout()                      # Toggle through layouts
                ),
            Key(
                [mod, "shift"], "q",
                lazy.window.kill()                      # Kill active window
                ),
            Key(
                [mod, "shift"], "r",
                lazy.restart()                          # Restart Qtile
                ),
            Key(
                [mod, "shift"], "e",
                lazy.shutdown()                         # Shutdown Qtile
                ),
            Key([mod], "w",
                lazy.to_screen(2)                       # Keyboard focus screen(0)
                ),
            Key([mod], "e",
                lazy.to_screen(0)                       # Keyboard focus screen(1)
                ),
            Key([mod], "r",
                lazy.to_screen(1)                       # Keyboard focus screen(2)
                ),
            Key([mod, "control"], "k",
                lazy.layout.section_up()                # Move up a section in treetab
                ),
            Key([mod, "control"], "j",
                lazy.layout.section_down()              # Move down a section in treetab
                ),
            ### Window controls
            Key(
                [mod], "k",
                lazy.layout.down()                      # Switch between windows in current stack pane
                ),
            Key(
                [mod], "j",
                lazy.layout.up()                        # Switch between windows in current stack pane
                ),
            Key(
                [mod, "shift"], "k",
                lazy.layout.shuffle_down()              # Move windows down in current stack
                ),
            Key(
                [mod, "shift"], "j",
                lazy.layout.shuffle_up()                # Move windows up in current stack
                ),
            Key(
                [mod, "shift"], "l",
                lazy.layout.grow(),                     # Grow size of current window (XmonadTall)
                lazy.layout.increase_nmaster(),         # Increase number in master pane (Tile)
                ),
            Key(
                [mod, "shift"], "h",
                lazy.layout.shrink(),                   # Shrink size of current window (XmonadTall)
                lazy.layout.decrease_nmaster(),         # Decrease number in master pane (Tile)
                ),
            Key(
                [mod, "shift"], "Left",                 # Move window to workspace to the left
                window_to_prev_group
                ),
            Key(
                [mod, "shift"], "Right",                # Move window to workspace to the right
                window_to_next_group
                ),
            Key(
                [mod], "n",
                lazy.layout.normalize()                 # Restore all windows to default size ratios 
                ),
            Key(
                [mod], "m",
                lazy.layout.maximize()                  # Toggle a window between minimum and maximum sizes
                ),
            Key(
                [mod, "shift"], "KP_Enter",
                lazy.window.toggle_floating()           # Toggle floating
                ),
            Key(
                [mod, "shift"], "space",
                lazy.layout.rotate(),                   # Swap panes of split stack (Stack)
                lazy.layout.flip()                      # Switch which side main pane occupies (XmonadTall)
                ),
            ### Stack controls
            Key(
                [mod], "space",
                lazy.layout.next()                      # Switch window focus to other pane(s) of stack
                ),
            Key(
                [mod, "control"], "Return",
                lazy.layout.toggle_split()              # Toggle between split and unsplit sides of stack
                ),
                
            ### Dmenu Run Launcher
            Key(
                [mod], "d",
                lazy.spawn("dmenu_run -fn 'UbuntuMono Nerd Font:size=10' -nb '#002b36' -nf '#93a1a1' -sb '#268bd2' -sf '#002b36' -p 'dmenu:'")
                ),
            Key(
                 [mod], "x", 
                 lazy.spawn("pcmanfm")
                 ),
            Key(
                [mod], "q",
                lazy.spawn("qutebrowser")
                )]
           
    return keys

##### BAR COLORS #####

def init_colors():
    return [["#002B36", "#002B36"], # panel background
            ["#DC322F", "#DC322F"], # background for current screen tab
            ["#93A1A1", "#93A1A1"], # font color for group names
            ["#DC322F", "#DC322F"], # background color for layout widget
            ["#000000", "#000000"], # background for other screen tabs
            ["#6C71C4", "#6C71C4"], # dark green gradiant for other screen tabs
            ["#859900", "#859900"], # background color for network widget
            ["#6C71C4", "#6C71C4"], # background color for pacman widget
            ["#9CC4FF", "#9CC4FF"], # background color for cmus widget
            ["#b58900", "#b58900"], # background color for clock widget
            ["#000000", "#000000"]] # background color for systray widget

##### GROUPS #####

def init_group_names():
    return [("DEV", {'layout': 'max'}),
            ("WWW", {'layout': 'max'}),
            ("GAMES", {'layout' : 'floating'}),
            ("SYS", {'layout': 'monadtall'}),
            ("DOC", {'layout': 'monadtall'}),
            ("VBOX", {'layout': 'floating'}),
            ("CHAT", {'layout': 'bsp'}),
            ("MEDIA", {'layout': 'monadtall'}),
            ("MUSIC", {'layout' : 'max'})]

def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]


##### LAYOUTS #####

def init_floating_layout():
    return layout.Floating(border_focus="#002B36")

def init_layout_theme():
    return {"border_width": 2,
            "margin": 10,
            "border_focus": "#6c71c4",
            "border_normal": "#002B36"
           }

def init_border_args():
    return {"border_width": 2}

def init_layouts():
    return [layout.Max(**layout_theme),
            layout.MonadTall(**layout_theme),
            layout.MonadWide(**layout_theme),
            layout.Bsp(**layout_theme),
            #layout.Stack(stacks=2, **layout_theme),
            #layout.Columns(**layout_theme),
            #layout.RatioTile(**layout_theme),
            #layout.VerticalTile(**layout_theme),
            #layout.Tile(shift_windows=True, **layout_theme),
            #layout.Matrix(**layout_theme),
            #layout.Zoomy(**layout_theme),
            layout.Floating(**layout_theme)]

##### WIDGETS #####

def init_widgets_defaults():
    return dict(font="Ubuntu Mono",
                fontsize = 11,
                padding = 2,
                background=colors[2])

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 0,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 1,
                        active = colors[2],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "block",
                        this_current_screen_border = colors[1],
                        this_screen_border = colors [4],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.Prompt(
                        prompt=prompt,
                        font="Ubuntu Mono",
                        padding=10,
                        foreground = colors[3],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.WindowName(font="Ubuntu",
                        fontsize = 11,
                        foreground = colors[5],
                        background = colors[0],
                        padding = 5
                        ),
                        
              
               widget.Image(
                        scale = True,
                        filename = "~/.config/qtile/memtobar.png",
                        background = colors [6]
                        ),
               widget.TextBox(
                        text=" ↯",
                        foreground=colors[0],
                        background=colors[6],
                        padding = 0,
                        fontsize=14
                        ),
               widget.Net(
                        interface = "enp1s0",
                        foreground = colors[0],
                        background = colors[6],
                        padding = 5
                        ),
               widget.Image(
                        scale = True,
                        filename = "~/.config/qtile/memtovief.png",
                        background = colors[6]
                        ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text=" ☵",
                        padding = 5,
                        foreground=colors[0],
                        background=colors[3],
                        fontsize=14
                        ),
               widget.CurrentLayout(
                        foreground = colors[0],
                        background = colors[3],
                        padding = 5
                        ),
               widget.Image(
                       scale = True,
                       filename = "~/.config/qtile/viewtoupdate.png",
                       background = colors[6]
                       ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text=" ⟳",
                        padding = 5,
                        foreground=colors[0],
                        background=colors[7],
                        fontsize=14
                        ),
               widget.Pacman(
                        execute = "urxvtc",
                        update_interval = 1800,
                        foreground = colors[0],
                        background = colors[7]
                        ),
               widget.TextBox(
                        text="Updates",
                        padding = 5,
                        foreground=colors[0],
                        background=colors[7]
						),
                widget.Image(
                        scale = True,
                        filename = "~/.config/qtile/updatetosystray.png",
                        background = colors [6]
                        ),
                widget.Systray(
                        background=colors[10],
                        padding = 5
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 5,
                        foreground = colors[0],
                        background = colors[10]
                        ),
               widget.Image(
                       scale = True,
                       filename = "~/.config/qtile/systraytoclock.png",
                       background = colors[6]
                       ),
               widget.TextBox(
                        font="Ubuntu Bold",
                        text=" 🕒",
                        foreground=colors[0],
                        background=colors[9],
                        padding = 5,
                        fontsize=14
                        ),
               widget.Clock(
                        foreground = colors[0],
                        background = colors[9],
                        format="%A, %B %d - %H:%M"
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 5,
                        foreground = colors[0],
                        background = colors[9]
                        )
              ]
    return widgets_list

##### SCREENS ##### (TRIPLE MONITOR SETUP)

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20))]

##### FLOATING WINDOWS #####

@hook.subscribe.client_new
def floating(window):
    floating_types = ['notification', 'toolbar', 'splash', 'dialog']
    transient = window.window.get_wm_transient_for()
    if window.window.get_wm_type() in floating_types or transient:
        window.floating = True

def init_mouse():
    return [Drag([mod], "Button1", lazy.window.set_position_floating(),      # Move floating windows
                 start=lazy.window.get_position()),
            Drag([mod], "Button3", lazy.window.set_size_floating(),          # Resize floating windows
                 start=lazy.window.get_size()),
            Click([mod, "shift"], "Button1", lazy.window.bring_to_front())]  # Bring floating window to front

##### DEFINING A FEW THINGS #####

if __name__ in ["config", "__main__"]:
    mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
    myTerm = "urxvt"                                    # My terminal of choice
    myConfig = "/home/martijn/.config/qtile/config.py"    # Qtile config file location 

    colors = init_colors()
    keys = init_keys()
    mouse = init_mouse()
    group_names = init_group_names()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layout_theme = init_layout_theme()
    border_args = init_border_args()
    layouts = init_layouts()
    screens = init_screens()
    widget_defaults = init_widgets_defaults()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

##### SETS GROUPS KEYBINDINGS #####

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))          # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Send current window to another group

#Define startup applications:
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
@hook.subscribe.startup
def runner():
    import subprocess
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
