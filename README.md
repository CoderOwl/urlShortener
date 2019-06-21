## urlShortener

Basic url shortener with customer short key to UppRL mapping. 

### How to run? 

Initialize the virtualenv `venv` and run `python server.py`. The application runs on port 5000 and the following are the endpoints:

`/`: Welcome screen

`/createUrl`: Form to submit short key to long url mapping. Example: short = fb long = https://www.facebook.com/

`/<short>`: Redirects to the long url if short key is found. 
