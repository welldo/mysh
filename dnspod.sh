#!/bin/sh
#

#############################################################
# AnripDdns v6.2.0
#
# Dynamic DNS using DNSPod API
#
# Author: Rehiy, https://github.com/rehiy
#                https://www.anrip.com/?s=dnspod
# Collaborators: ProfFan, https://github.com/ProfFan
#
# Usage: please refer to `ddnspod.sh`
#
#############################################################

export arToken

# Define arLog to output to stderr, if not defined in ddnspod.sh

if ! type arLog >/dev/null 2>&1; then
    arLog() {
        >&2 echo $@
    }
fi

# The url to be used for querying public ipv6 address. We set a default here.

if [ -z "$arIp6QueryUrl" ]; then
    arIp6QueryUrl="http://ipv6.rpc.im/ip"
fi

# The error code to return when a ddns record is not changed

if [ -z "$arErrCodeUnchanged" ]; then
    arErrCodeUnchanged=0 # By default, report unchanged event as success
fi

# Get IPv4

arWanIp4() {

    local hostIp

    local lanIps="^$"

    lanIps="$lanIps|(^10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)"
    lanIps="$lanIps|(^127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)"
    lanIps="$lanIps|(^169\.254\.[0-9]{1,3}\.[0-9]{1,3}$)"
    lanIps="$lanIps|(^172\.(1[6-9]|2[0-9]|3[0-1])\.[0-9]{1,3}\.[0-9]{1,3}$)"
    lanIps="$lanIps|(^192\.168\.[0-9]{1,3}\.[0-9]{1,3}$)"
    lanIps="$lanIps|(^100\.(6[4-9]|[7-9][0-9])\.[0-9]{1,3}\.[0-9]{1,3}$)"  # 100.64.x.x - 100.99.x.x
    lanIps="$lanIps|(^100\.1([0-1][0-9]|2[0-7])\.[0-9]{1,3}\.[0-9]{1,3}$)" # 100.100.x.x - 100.127.x.x

    case $(uname) in
        'Linux')
            hostIp=$(ip -o -4 route get 100.64.0.1 | grep -oE 'src [0-9\.]+' | awk '{print $2}' | grep -Ev "$lanIps")
        ;;
        Darwin|FreeBSD)
            hostIp=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | grep -Ev "$lanIps")
        ;;
    esac

    if [ -z "$hostIp" ]; then
        return 1
    fi

    if [ -z "$(echo $hostIp | grep -E '^[0-9\.]+$')" ]; then
        return 1
    fi

    echo $hostIp

}

# Get IPv6

arWanIp6() {

    local hostIp

    local lanIps="(^$)|(^::1$)|(^fe[8-9,A-F])"

    case $(uname) in
        'Linux')
            hostIp=$(ip -o -6 route get 100::1 | grep -oE 'src [0-9a-fA-F:]+' | awk '{print $2}' | grep -Ev "$lanIps")
        ;;
    esac

    if [ -z "$hostIp" ]; then
        if type curl >/dev/null 2>&1; then
            hostIp=$(curl -6 -s $arIp6QueryUrl)
        elif ! wget --help 2>&1 | grep -qs BusyBox; then
            hostIp=$(wget -6 -q -O- $arIp6QueryUrl)
        else
            hostIp=$(wget -q -O- $arIp6QueryUrl)
        fi
    fi

    if [ -z "$hostIp" ]; then
        arLog "> arWanIp6 - Can't get ip address"
        return 1
    fi

    if [ -z "$(echo $hostIp | grep -E '^[0-9a-fA-F:]+$')" ]; then
        arLog "> arWanIp6 - Invalid ip address"
        return 1
    fi

    echo $hostIp

}

# Dnspod Bridge
# Args: interface data

arDdnsApi() {

    local agent="AnripDdns/6.2.0(wang@rehiy.com)"

    local dnsapi="https://dnsapi.cn/${1:?'Info.Version'}"
    local params="login_token=$arToken&format=json&lang=en&$2"

    if type curl >/dev/null 2>&1; then
        curl -4 -s -A $agent -d $params $dnsapi
    elif ! wget --help 2>&1 | grep -qs BusyBox; then
        wget -4 -q -O- --no-check-certificate -U $agent --post-data $params $dnsapi
    else
        wget -q -O- --no-check-certificate -U $agent --post-data $params $dnsapi
    fi

}

# Fetch Record Id
# Args: domain subdomain recordType

arDdnsLookup() {

    local errMsg

    local recordId

    # Get Record Id
    recordId=$(arDdnsApi "Record.List" "domain=$1&sub_domain=$2&record_type=$3")
    recordId=$(echo $recordId | sed 's/.*"id":"\([0-9]*\)".*/\1/')

    if ! [ "$recordId" -gt 0 ] 2>/dev/null ;then
        errMsg=$(echo $recordId | sed 's/.*"message":"\([^\"]*\)".*/\1/')
        arLog "> arDdnsLookup - $errMsg"
        return 1
    fi

    echo $recordId
}

# Update Record Value
# Args: domain subdomain recordId recordType [hostIp]

arDdnsUpdate() {

    local errMsg

    local lastRecordIp
    local recordRs
    local recordCd
    local recordIp

    # if code for unchanged event is specified to be different from updated event, we fetch the last record ip
    if [ $arErrCodeUnchanged -ne 0 ]; then
        recordRs=$(arDdnsApi "Record.Info" "domain=$1&record_id=$3")
        recordCd=$(echo $recordRs | sed 's/.*{"code":"\([0-9]*\)".*/\1/')
        lastRecordIp=$(echo $recordRs | sed 's/.*,"value":"\([0-9a-fA-F\.\:]*\)".*/\1/')

        if [ "$recordCd" != "1" ]; then
            errMsg=$(echo $recordRs | sed 's/.*,"message":"\([^"]*\)".*/\1/')
            arLog "> arDdnsUpdate - error: $errMsg"
            return 1
        else
            arLog "> arDdnsUpdate - last record ip: $lastRecordIp"
        fi
    fi

    # update ip
    if [ -z "$5" ]; then
        recordRs=$(arDdnsApi "Record.Ddns" "domain=$1&sub_domain=$2&record_id=$3&record_type=$4&record_line=%e9%bb%98%e8%ae%a4")
    else
        recordRs=$(arDdnsApi "Record.Ddns" "domain=$1&sub_domain=$2&record_id=$3&record_type=$4&value=$5&record_line=%e9%bb%98%e8%ae%a4")
    fi

    # parse result
    recordCd=$(echo $recordRs | sed 's/.*{"code":"\([0-9]*\)".*/\1/')
    recordIp=$(echo $recordRs | sed 's/.*,"value":"\([0-9a-fA-F\.\:]*\)".*/\1/')

    if [ "$recordCd" != "1" ]; then
        errMsg=$(echo $recordRs | sed 's/.*,"message":"\([^"]*\)".*/\1/')
        arLog "> arDdnsUpdate - error: $errMsg"
        return 1
    elif [ $arErrCodeUnchanged -eq 0 ]; then
        arLog "> arDdnsUpdate - success: $recordIp" # both unchanged and updated event
        echo $recordIp
        return 0
    elif [ "$recordIp" = "$lastRecordIp" ]; then
        arLog "> arDdnsUpdate - unchanged: $recordIp" # unchanged event
        echo $recordIp
        return $arErrCodeUnchanged
    else
        arLog "> arDdnsUpdate - updated: $recordIp" # updated event
        echo $recordIp
        return 0
    fi

}

# DDNS Check
# Args: domain subdomain [6|4]

arDdnsCheck() {

    local hostIp

    local recordId
    local recordType

    arLog "=== Check $2.$1 ==="
    arLog "Fetching Host Ip"

    if [ "$3" = "6" ]; then
        recordType=AAAA
        hostIp=$(arWanIp6)
        if [ $? -ne 0 ]; then
            arLog $hostIp
            return 1
        else
            arLog "> Host Ip: $hostIp"
            arLog "> Record Type: $recordType"
        fi
    else
        recordType=A
        hostIp=$(arWanIp4)
        if [ $? -ne 0 ]; then
            arLog "> Host Ip: Auto"
            arLog "> Record Type: $recordType"
        else
            arLog "> Host Ip: $hostIp"
            arLog "> Record Type: $recordType"
        fi
    fi

    arLog "Fetching RecordId"
    recordId=$(arDdnsLookup "$1" "$2" "$recordType")

    if [ $? -ne 0 ]; then
        arLog $recordId
        return 1
    else
        arLog "> Record Id: $recordId"
    fi

    arLog "Updating Record value"
    arDdnsUpdate "$1" "$2" "$recordId" "$recordType" "$hostIp"

}
arToken="339991,a4943fdc171eb22969712733c81ba1a8"
arDdnsCheck "hiyang.ltd" "db"
arDdnsCheck "sayang.ltd" "db"
arDdnsCheck "hiyang.ltd" "dm"
arDdnsCheck "sayang.ltd" "dm"

