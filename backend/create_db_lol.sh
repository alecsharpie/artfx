#!/bin/zsh
echo '[]' > init_DB.json
gsutil cp DB.json gs://website-assets-alecsharpie/artfx/DB.json
