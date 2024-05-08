


docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash \
  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"

python -m virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt

zip -r enigma.zip virtualenv __main__.py
nuv -wsk action delete /dmaggiorotto/Test/enigma 


nuv -wsk action create /dmaggiorotto/Test/enigma --kind python:36  --web true  enigma.zip

###
docker run --rm -v "$PWD:/tmp" --platform linux/amd64 python:3.11.9-bullseye bash -c "cd tmp && pip install virtualenv && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
rmenigma.zip ; zip -r enigma.zip virtualenv __main__.py
nuv -wsk action update /dmaggiorotto/Test/enigma --kind python:3.11  --web true  enigma.zip
###

nuv url /dmaggiorotto/Test/enigma

https://nuvolaris.dev/api/v1/web/dmaggiorotto/Test/enigma

https://nuvolaris.dev/api/v1/namespaces/_/actions/enigma?blocking=true&result=true

https://nuvolaris.dev/api/v1/web/denis.maggiorotto@sunnyvale_it/Test/enigma.json



zip -j -r enigma | docker run -i openwhisk/action-python-v3.11 -compile main > enigma.zip

cat ~/.wskprops
. ~/.wskprops

nuv -wsk namespace list -v

nuv -wsk action list -v



curl -u $AUTH  https://nuvolaris.dev/api/v1/namespaces/_/limits





curl -X 'POST' \
  'https://nuvolaris.dev/api/v1/web/dmaggiorotto/Test/enigma/I/encrypt' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "plugboard": {
    "wirings": [
      {
        "from_letter": "D",
        "to_letter": "Z"
      }
    ]
  },
  "auto_increment_rotors": true,
  "cleartext": "DENIS",
  "rotors": [
    {
      "position": 1,
      "ring": 0,
      "type": "I"
    },
    {
      "position": 0,
      "ring": 0,
      "type": "I"
    },
    {
      "position": 0,
      "ring": 0,
      "type": "I"
    }
  ],
  "reflector": "UKW-A"
}'