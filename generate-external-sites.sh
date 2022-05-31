#!/bin/bash

sqlite3 atk.sqlite "select distinct name from atk_allsites;" | while read BABE ; do echo $BABE ; ./external-sites.sh "$BABE" sql; done

