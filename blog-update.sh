#!/bin/bash

echo "=========`date`========"

#sqlite3 /var/www/html/atk/atk.sqlite "CREATE TABLE babes ( id int unique, gallery varchar(100), name varchar(50), model varchar(100), link varchar(200), date varchar(8), age int, pob varchar(50), occ varchar(50), file varchar(50), tn varchar(50), tags varchar(1000) );"
#sqlite3 /var/www/html/atk/atk.sqlite "delete from babes;"

convert_date () {
    local months=( January February March April May June July August September October November December )
    local i
    for (( i=0; i<11; i++ )); do
        [[ $2 = ${months[$i]} ]] && break
    done
    printf "%4d%02d%02d\n" $3 $(( i+1 )) $1
}

#PAGE=1
for PAGE in `seq 1 500` ; do
  URL="https://www.atkmodels.com/blog/page/${PAGE}/"
  if [ "$PAGE" -eq 1 ]; then
    URL="https://www.atkmodels.com/blog/"
  fi
  curl -s "$URL" > index.html
  for GALLERY in `grep posttitle index.html | gawk -F"a href=" '{ print $2 }' | gawk -F"\"" '{ print $2 }'`; do
    curl -s "$GALLERY" > babe.html
    MODEL=`grep '<span>Model</span>' babe.html | gawk -F"<span>Model</span>" '{ print $2 }' | gawk -F"\"" '{ print $2 }'`
    NAME=`grep '<span>Model</span>' babe.html | gawk -F"<span>Model</span>" '{ print $2 }' | gawk -F"[><]" '{ print $3 }' | sed -e "s/'/\"/g"`
    if echo $NAME | grep -e " [0-9]$" > /dev/null; then
      echo "$NAME -> remove digit from name"
      NAME=${NAME::-2}
      echo "new name: $NAME"
    fi
    LINK=`grep '<span>Model</span>' babe.html | gawk -F"<span>Model</span>" '{ print $2 }' | sed -e 's# : ##' | sed -e 's/<br>//g' | sed -e 's/ rel="tag"//g' | sed -e "s#'#\"#g" | gawk -F"<span>" '{ print $1 }'`
    DATE=`grep 'postinfo' babe.html | gawk -F"postinfo\">" '{ print $2 }' | gawk -F"," '{ print $1 }'`
    DATE=$( convert_date $DATE )
    AGE=`grep '<span>Age</span>' babe.html | gawk -F "<span>Age</span> : " '{ print $2 }' | gawk -F"<" '{ print $1 }'`
    POB=`grep '<span>Place Of Birth</span>' babe.html | gawk -F "<span>Place Of Birth</span> : " '{ print $2 }' | gawk -F"<" '{ print $1 }'` | sed -e "s/'/\\\'/g"
    OCC=`grep '<span>Occupation</span>' babe.html | gawk -F "<span>Occupation</span> : " '{ print $2 }' | gawk -F"<" '{ print $1 }'` | sed -e "s/'/\\\'/g"
    TAGS=""
    for TAG in `grep 'Tags:' babe.html | gawk -F"Tags:" '{ print $2 }' | sed -e 's/,/\n/g' | gawk -F"\"" '{ print $2 }' ` ; do TAGS="$TAGS|$TAG" ; done
    TAGS=`echo $TAGS | sed 's/^|\(.*\)/\1/'`
    PIC_URL=`grep "http.://www.atkmodels.com/blog/galleries/" babe.html | grep '\-1.html' | gawk -F"href=" '{ print $2 }' | gawk -F"['\"]" '{ print $2 }' | sed -e 's/ /%20/g'`
    ID=`grep "http.://www.atkmodels.com/blog/galleries/" babe.html | grep '\-1.html' | gawk -F"href=" '{ print $2 }' | gawk -F"['\"]" '{ print $2 }' | gawk -F"_" '{ print $NF }' | gawk -F"-" '{ print $1 }'`
    ID=$((ID+10000000))
    curl -s "$PIC_URL" > pic.html
    PIC=`grep -i '_big.jpg' pic.html | gawk -F"src='" '{ print $2 }' | gawk -F"'" '{ print $1 }'`
    FILE=`grep -i '_big.jpg' pic.html | gawk -F"src='" '{ print $2 }' | gawk -F"'" '{ print $1 }' | gawk -F"galleries/" '{ print $2 }' | sed -e 's#/#+#g'`
    TN_URL=`grep "http.://www.atkmodels.com/blog/galleries/" babe.html | grep '\-1.html' | gawk -F"src=" '{ print $2 }' | gawk -F"['\"]" '{ print $2 }'`
    TN=`grep "http.://www.atkmodels.com/blog/galleries/" babe.html | grep '\-1.html' | gawk -F"src=" '{ print $2 }' | gawk -F"['\"]" '{ print $2 }' | gawk -F"galleries/" '{ print $2 }' | sed -e 's#/#+#g'`
    echo "Page: $PAGE"
    echo "Gal: $GALLERY"
    echo "Model: $MODEL"
    echo "Link: $LINK"
    echo "Name: $NAME"
    echo "ID: $ID"
    echo "Date: $DATE"
    echo "File: $FILE"
    echo "TN: $TN"
    echo "Age: $AGE"
    echo "Place: $POB"
    echo "Occupation: $OCC"
    echo "Tags: $TAGS"

    QUERY=`echo "INSERT INTO atk_babe (id, gallery, name, model, link, date, age, pob, occ, file, tn, tags, likes, monthlikes, duellikes) VALUES ($ID,'$GALLERY','$NAME','$MODEL','$LINK','$DATE','$AGE','$POB','$OCC','$FILE','$TN','$TAGS', 0, 0, 0);" | sed -e "s/''/null/g"`
    echo $QUERY
    RESPONSE=`sqlite3 atk.sqlite "$QUERY" 2>&1`
    echo "DB RESP: $RESPONSE"
    if [[ "$RESPONSE" == *"UNIQUE constraint failed"* ]]; then
        echo already in db - exiting
        exit 0
    elif [[ "$RESPONSE" == *"Error"* ]]; then
        echo "ERR: issue with writting to db - exiting"
        echo -e "Subject: [$HOSTNAME] blog-update.sh - ERR: issue with writting to db\n\n$RESPONSE\n" | sendmail art.root@gmail.com
        exit 1
    else
        echo ok
        echo "external-sites.sh"
        #20240925 - disabling as those sites doesn't seem to work anymore
        #20241031 - fixed, but results are quite shitty
        ./external-sites.sh "$NAME" sql &
        echo "DISABLED"
    fi
  done
done

