# Configuring aws CLi(after installing)  
aws configure

# uploading data into s3 bucket
  # 1. Statstic reference data (Json files)
aws s3 cp . s3://end-to-end-youtube-de-project1/youtube/raw-statics-data --recursive --exclude "*" --include "*.json"
  
  # 2. Raw data the CSV files
  
aws s3 cp CAvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=ca/
aws s3 cp DEvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=de/
aws s3 cp FRvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=fr/
aws s3 cp GBvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=gb/
aws s3 cp INvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=in/
aws s3 cp JPvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=jp/
aws s3 cp KRvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=kr/
aws s3 cp MXvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=mx/
aws s3 cp RUvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=ru/
aws s3 cp USvideos.csv s3://end-to-end-youtube-de-project1/youtube/raw-statics-data/region=us/
