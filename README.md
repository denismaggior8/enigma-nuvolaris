


docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash \
  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
zip -r enigma.zip virtualenv __main__.py
nuv -wsk action delete enigma 
nuv -wsk action create enigma --kind python:3  --web true enigma.zip



https://nuvolaris.dev/api/v1/namespaces/_/actions/enigma?blocking=true&result=true

cat ~/.wskprops
. ~/.wskprops

nuv -wsk namespace list -v




curl -u $AUTH  https://nuvolaris.dev/api/v1/namespaces/_/limits