#!/bin/bash

if [ $# -ne 2 ]; then
    echo "usage: $0 <model> <print|sql>"
    exit 2
fi

if [ ! -f external-sites.txt ]; then
    echo "external-sites.txt not found"
    exit 1
fi

#BABE=$(echo $1 | sed -e 's/-/ /g')
BABE="$1"
URLBABE=$(echo $1 | tr '[:upper:]' '[:lower:]' | sed -e 's/ /-/g')
BABELETTER=$(echo $URLBABE | cut -c 1-1)

URLS=''
for SITE in $(cat external-sites.txt); do
    URL="https://$SITE/pornstar/$BABELETTER"
    #echo $URL
    CURL=$(curl --silent "$URL" | grep "https://${SITE}/pornstar/$URLBABE")
    #echo "$CURL"
    if [ "$CURL" ]; then
        NUM=$(curl --silent "https://${SITE}/pornstar/$URLBABE" | grep "<a href=\"https://${SITE}/" | wc -l)
        #echo $NUM
        URLS="${URLS}${SITE};${NUM}|"
    fi
done

# 20230813 - disabled, site seems to be down
#for www.hairy.today
#CURL=$(curl --silent "http://www.hairy.today/pornstar/$URLBABE")
#if echo "$CURL" | grep "clips found" &>/dev/null; then
#    NUM=$(echo $CURL | grep "clips found" | gawk -F "clips found" ' { print $2 }' | gawk -F "<" '{ print $1 }' | tr -d " ")
#    URLS="${URLS}${SITE};${NUM}|"
#fi

URLS=`echo $URLS | sed 's/.$//'`

if [ "$URLS" ]; then
    echo $URLS
    if [ "$2" == "sql" ]; then
        #echo "insert or replace into atk_externalsite (name,urls) values ('$BABE','$URLS');"
        sqlite3 atk.sqlite "insert or replace into atk_externalsite (name,urls) values ('$BABE','$URLS');"
    fi
else
    sqlite3 atk.sqlite "delete from atk_externalsite where name='$BABE';"
    exit 0
fi

