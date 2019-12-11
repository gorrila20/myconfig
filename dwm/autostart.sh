xrdb ~/.Xresources
picom&
nitrogen --restore&
dunst&
volumeicon&
nm-applet&
blueman&
parcellite&
~/.config/statusbar.sh&
xautolock -detectsleep -time 3 -corners -000 -locker "i3lock -i /usr/share/backgrounds/gnome/river.png"   -notify 30   -notifier "notify-send -u critical -t 10000 -- 'LOCKING screen in 30 seconds'"&
