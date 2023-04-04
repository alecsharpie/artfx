#!bin/zsh
gsutil cors set bucket_cors.json gs://website-assets-alecsharpie
gsutil cors get gs://website-assets-alecsharpie
