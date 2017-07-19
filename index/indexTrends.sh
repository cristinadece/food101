for f in /home/foodmap/data/food-tweets/food-tweets-2017-03*;
do
  python index/index_trend.py -f $f -i trend -img /home/foodmap/data/img_classification/twitter.03.report.tsv
  sleep 1m
done
