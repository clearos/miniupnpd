#!/bin/sh

#
# Prep the parameters to pass to systemd
#

# Source networking configuration.
. /etc/clearos/network.conf

# Source miniupnpd_clearos.conf configuration.
. /etc/miniupnpd/miniupnpd_clearos.conf

# Determine WAN interface default route
MINIUPNPD_WAN="-i `LC_ALL=C ip -4 route | grep 'default' | sed -e 's/.*dev[[:space:]]*//' -e 's/[[:space:]].*//'`"

# kludge for when WAN goes down to stop miniupnpd failing
if [ "$MINIUPNPD_WAN" = "-i " ]; then
	MINIUPNPD_WAN="-i lo"
fi

# List all the LAN's with the correct config parameter
MINIUPNPD_LANS=""
for LAN in $LANIF; do
	MINIUPNPD_LANS="$MINIUPNPD_LANS-a $LAN "
done

if [ "$USE_HOTLAN" = "yes" -a ! -z "$HOTIF" ]; then
	MINIUPNPD_LANS="$MINIUPNPD_LANS-a $HOTIF "
fi

# Should really be done as part of the installation. Done here for safety.
[ -f /var/lib/miniupnpd/upnp.leases ] || touch /var/lib/miniupnpd/upnp.leases

systemctl set-environment MINIUPNPD_START_OPTIONS="$MINIUPNPD_WAN $MINIUPNPD_LANS $MINIUPNPD_OPTIONS"

exit 0



