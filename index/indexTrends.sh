for f in /home/foodmap/data/food-tweets/food-tweets-2017-03*;
do
  python index/index_trend.py -f $f -i trend
  sleep 1m
done
