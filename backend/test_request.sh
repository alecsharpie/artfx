#!bin/zsh
curl -m 70 -X GET https://artfx-generator-rwkn37xpsq-uc.a.run.app \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json"
