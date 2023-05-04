#!/bin/zsh
gcloud functions deploy artfx_generator --timeout=120 --trigger-http --runtime=python310 --source=google-cloud-function.py --entry-point=upload_generation --region=asia-east1
```
