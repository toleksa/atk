#!/bin/bash

echo "=========`date`========"

for DAYS in `seq 0 3650`; do
    DATE=$(date  --date="$DAYS days ago" +%y%m%d)
    if [ "$DATE" == "120101" ]; then
        echo "1201010 - that's enough"
        exit 0;
    fi
    ERR=0
    for SITE in exotics galleria hairy
    do
        LINK="https://www.atkmodels.com/$SITE/index.php?day=$DATE"
        NAME=$(curl --silent "$LINK" | grep "for your pleasure" | gawk -F"we present" '{ print $2 }' | gawk -F"<b>" '{ print $2 }' | gawk -F"</b>" '{ print $1 }' | xargs)
        echo $DATE $SITE
        if [ "$NAME" != "" ]; then
            echo ${NAME}
            #if [ ! -f "pics/$SITE/${DATE}_1.jpg" ]; then
            #    wget -q -O pics/$SITE/${DATE}_1.jpg "http://www.atkmodels.com/$SITE/img/content/${DATE}_1.jpg"
            #fi
            #if [ ! -f "pics/$SITE/${DATE}_7.jpg" ]; then
            #    wget -q -O pics/$SITE/${DATE}_7.jpg "http://www.atkmodels.com/$SITE/img/content/${DATE}_7.jpg"
            #fi
            QUERY="insert into atk_sitebabe (id, date, name, site, tags, likes, monthlikes, duellikes) values(null,'$DATE','$NAME','$SITE','',0,0,0);"
            echo $QUERY
            RESPONSE=`sqlite3 atk.sqlite "$QUERY" 2>&1`
            echo "DB RESP: $RESPONSE"
            if [[ "$RESPONSE" == *"UNIQUE constraint failed"* ]]; then
                ERR=$((ERR+1))
                echo already in db - ERR:$ERR
                #exit 0
            else
                echo ok
                echo "external-sites.sh"
                ./external-sites.sh "$NAME" sql
            fi
            QUERY="update atk_sitebabe set name = '$NAME' where date='$DATE' and site='$SITE';"
            echo $QUERY
            sqlite3 atk.sqlite "$QUERY" 2>&1
        else
            echo no-name
        fi
        if [ $ERR -eq 3 ]; then
            echo "ERR==3: all 3 sites already in db - exiting"
            exit 0
        fi
    done
    
done

