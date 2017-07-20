for f in /home/foodmap/data/food-tweets/food-tweets-2017-05*;
do
  python index/index_trend.py -f $f -i trend -img /home/foodmap/data/img_classification/twitter.05.report.tsv
  sleep 1m
done
