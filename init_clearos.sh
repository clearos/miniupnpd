#!/bin/sh

#
# Prep the parameters to pass to systemd
#

# Source networking configuration.
. /etc/clearos/network.conf

# Determine WAN interface default route
MINIUPNPD_WAN="-i `LC_ALL=C ip -4 route | grep 'default' | sed -e 's/.*dev[[:space:]]*//' -e 's/[[:space:]].*//'`"

# List all the LAN's with the correct config parameter
MINIUPNPD_LANS=""
for LAN in $LANIF; do
	MINIUPNPD_LANS="$MINIUPNPD_LANS-a $LAN "
done

# To include the HotLAN, uncomment the next line:
# MINIUPNPD_LANS="$MINIUPNPD_LANS-a $HOTIF "

# Set extra manually configured options here:
MINIUPNPD_OPTIONS=""

# Should really be done as part of the installation. Done here for safety.
[ -f /var/lib/miniupnpd/upnp.leases ] || touch /var/lib/miniupnpd/upnp.leases

systemctl set-environment MINIUPNPD_OPTIONS="$MINIUPNPD_WAN $MINIUPNPD_LANS $MINIUPNPD_OPTIONS"

exit 0



