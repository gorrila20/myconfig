#!/usr/bin/env sh

# Habdle SIGTRAP signals send by refbar to update statusbar immediately
trap update 5

# delimiter that is input between bar modules
delimiter=" | "

# main status function
status() { \
	printf " "
	# --- Some basic modules --- #
	# backligt module
	#let "backlight_percentage=$(cat /sys/class/backlight/intel_backlight/brightness) * 100 / $(cat /sys/class/backlight/intel_backlight/max_brightness)"
	#printf " $backlight_percentage%% "

	# Sound module
	amixer get Master | grep -o '\[on\]\|\[off\]\|[0-9]*%' | sed 's/\[on\]//;s/\[off\]//' | tr '\n' ' ' | awk '{ print $2 " " $1 }'

	# Wifi module
	if [ $(cat /sys/class/net/wlp5s0/operstate) == "up" ]; then
		printf " $(nmcli connection show --active | sed -n '1!p' | awk -F ' {2,}' '{print $1}')"
	else
		printf " No connection"
	fi

	printf "$delimiter"

	# battery module
	#for i in /sys/class/power_supply/BAT?/capacity; do
	#	if [ $(cat /sys/class/power_supply/BAT?/status) == "Discharging" ]; then
	#		case "$(cat $i)" in
	#			100|9[0-9]|8[0-9])	printf " $(cat $i)%%" ;;
	#			7[0-9]|6[0-9]|5[0-9])	printf " $(cat $i)%%" ;;
	#			4[0-9]|3[0-9]|2[0-9])	printf " $(cat $i)%%" ;;
	#			*)			printf " $(cat $i)%%" ;;
	#		esac
	#	else
	#		printf " $(cat $i)%%"
	#	fi
	#done && printf "$delimiter"

	#  --- Block of system statistics --- #
	# Memory
	let "mem=$(free | awk '/^Mem:/ {print $3}') * 100 / $(free | awk '/^Mem:/ {print $2}')"
	printf " $mem%% "

	# used CPU percentage
	printf " "
 	ps axch -o cmd:15,%cpu --sort=-%cpu | sed 21q | awk -F ' {2,}' '{usage+=$2} END {print usage "%"}'

	# CPU temperature
	printf " "
	temp="$(cat /sys/class/thermal/thermal_zone2/temp | sed 's/...$//')°C"
	printf "$temp"
	printf "$delimiter"

	# -- Time --- #
	printf " $(date '+%a %d-%m-%Y %H:%M') "
	}

update() { \
		xsetroot -name "$(status | tr '\n' ' ')" &
	wait
	}

while :; do
	update
		sleep 1m &
	wait
done
