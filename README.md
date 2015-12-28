# slackbot

## Installation
In your repo folder, create a file named 'config.ini', and paste below text in it
```
[ichef]
token=<your_slack_token>
```
Then, run below
```
pip install -r r.txt
```

## Usage
```
python test.py
```
How to add new feature？

1. Add new python file for your feature.
2. At top in test.py, add your keyword and the function you want to execute when message user types match the keyword to KEYWORD_LIST. If there are multiple keyword, use cama to split. EX: '電影,新片'
3. In your python feature file, import response.py and use the Response class as return value, like below
```
return Response(text="Hi! iCHEF! Go Beyond")
```


