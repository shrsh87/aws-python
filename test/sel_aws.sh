#!/bin/bash
 
for ((i=1; i<=10; i++))
do
  curl -X GET -d '{"col1": "'$i'" }' -H "Content-Type: application/json" http://my-alb-d215ca5-1880688837.ap-northeast-2.elb.amazonaws.com/users
  echo
	     
  #echo $i
done
