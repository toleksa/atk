#!/bin/bash

sqlite3 atk.sqlite "select count(*) from atk_allsites;"
sqlite3 atk.sqlite "select name,count(name) as c from atk_allsites group by name order by c desc LIMIT 20;"

