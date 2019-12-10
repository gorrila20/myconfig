#!/bin/sh
picom&
xrdb ~/.Xresources&
nm-applet&
volumeicon&
/usr/bin/dunst&
parcellite&
nitrogen --restore&
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1&
blueman-applet&
cbatticon&
xautolock -detectsleep -time 3 -corners -000 -locker "i3lock -i /usr/share/backgrounds/gnome/solar.png"   -notify 30   -notifier "notify-send -u critical -t 10000 -- 'LOCKING screen in 30 seconds'"&
