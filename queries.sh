#!/bin/bash

sqlite3 atk.sqlite "select count(*) from atk_babe;"
sqlite3 atk.sqlite "select age,count(age) from atk_babe group by age;"
sqlite3 atk.sqlite "select name,count(model) as c from atk_babe group by model order by c desc LIMIT 20;"

