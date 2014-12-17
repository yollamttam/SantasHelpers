mysql -u pymorph -ppymorph Santa -e "select * from toys where duration between 2.5*60  and 24*60 order by duration desc;" > good_jobs.csv
mysql -u pymorph -ppymorph Santa -e "select * from toys where duration > 24*60 order by duration desc;" > big_jobs.csv
mysql -u pymorph -ppymorph Santa -e "select * from toys where duration < 2.5*60 order by duration desc;" > tiny_jobs.csv



mysql -u pymorph -ppymorph Santa -e "select a.* from (select * from toys where duration between 2.5*60  and 24*60 order by rand(20) limit 144800) as a order by a.duration desc;" > good_test.csv
mysql -u pymorph -ppymorph Santa -e "select a.* from (select * from toys where duration > 24*60 order by rand(30) limit 214200) as a order by a.duration desc;" > big_test.csv
mysql -u pymorph -ppymorph Santa -e "select a.* from (select * from toys where duration < 2.5*60  order by rand(40) limit 640800) as a order by a.duration desc;" > tiny_test.csv

cat tiny_test.csv > all_test.csv
tail --lines=+2 good_test.csv >> all_test.csv
tail --lines=+2 big_test.csv >> all_test.csv
sed "s/\t/,/g" all_test.csv > all_test.bak
sed "s/:/ /g" all_test.bak > all_test.csv
sed "s/-/ /g" all_test.csv > all_test.bak
mv all_test.bak all_test.csv