To run the instance app separately from the pipeline in src/sample_app: 

Locally:
run `python placeholder.py`

Send a POST request to "0.0.0.0:5000" 
with body: 
`{"key": "SAMPLE_KEY",
    "intValue": 40
 }`

With Docker:
docker build -t app .
docker run --rm -p 5000:5000 app:latest

Send a POST request to "0.0.0.0:5000" 
with post body: 
`{"key": "SAMPLE_KEY",
    "intValue": 40
 }`