for f in /home/foodmap/data/food-tweets/food-tweets-2017-04*;
do
  python index/index_trend.py -f $f -i trends04
done