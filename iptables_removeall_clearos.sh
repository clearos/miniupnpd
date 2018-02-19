#!/bin/sh

#
# Tidy up the firewall, removing all MINIUPNPD chains and rules
#
TABLES="filter mangle nat"
IPTABLES=$(which iptables)

[ -z "$FW_PROTO" ] && FW_PROTO=ipv4
if [ "$FW_PROTO" == "ipv6" ]; then
    IPTABLES=$(which ip6tables)
fi

function get_all_chains()
{
    ${IPTABLES} -nw -L -t $1 | egrep '^Chain' | awk '{ print $2}'
}

function get_miniupnp_rules()
{
    ${IPTABLES} -nw --line-numbers -t $1 -L $2 |\
        egrep -v '^Chain' | grep MINIUPNP | awk '{ print $1 }' | sort -rn
}

function get_miniupnp_chains()
{
    ${IPTABLES} -nw -t $1 -L | egrep '^Chain' | grep MINIUPNP | awk '{ print $2 }'
}

for table in $TABLES; do
    CHAINS=$(get_all_chains ${table})
    [ -z "$CHAINS" ] && continue

    for chain in $CHAINS; do
        RULE_IDS=$(get_miniupnp_rules ${table} ${chain})
        [ -z "$RULE_IDS" ] && continue

        for rule_id in $RULE_IDS; do
            ${IPTABLES} -w -t ${table} -D ${chain} ${rule_id}
        done
    done


    CHAINS=$(get_miniupnp_chains ${table})
    [ -z "$CHAINS" ] && break

    for chain in $CHAINS; do
        ${IPTABLES} -w -t $table -F $chain && ${IPTABLES} -w -t $table -X $chain
    done
done

exit 0



