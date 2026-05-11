Memo: Key Python Web Libraries
1. Uvicorn (The Server)
   Role: Runs your web application.
   Usage: The "engine" that listens for incoming web traffic (essential for FastAPI/Starlette).
   Key Feature: Extremely fast and supports asynchronous tasks.
2. Requests (The Client)
   Role: Sends data to other websites/APIs.
   Usage: Use this when your code needs to "call" another service to get or send information.
   Key Feature: Makes complex HTTP communication very simple.
3. python-dotenv (The Config)
   Role: Manages secrets and settings.
   Usage: Loads variables from a .env file into your app.
   Key Feature: Keeps sensitive data (like API keys) out of your source code for better security.

How it all works together:
1. python-dotenv grabs your API_SECRET_KEY from the hidden file so you don't have to type it directly in your code.
2. Requests reaches out to api.agify.io (an external service) to fetch data whenever someone visits your /check-age/ link.
3. Uvicorn sits in the background, keeping the script running and listening for you to visit http://127.0.0.1:8000 in your browser.


routes: API endpoints
services: business logic
models: request schemas
core: configs/logging

********************
FAST API
A high-performance Python web framework for building APIs. 
It is built on Starlette (for web handling) and 
Pydantic (for data validation), running on the Uvicorn server.

Why use it?
-Speed: One of the fastest Python frameworks (async-ready).
-Auto-Docs: Automatically generates interactive testing pages at /docs.
-Safety: Uses Python Type Hints to catch errors and validate data automatically.
-Developer Friendly: Provides excellent editor autocompletion and clear error messages.

How to Run & Test
-Run command: fastapi dev main.py (or uvicorn main:app --reload).
-Default URL: http://127.0.0.1:8000.
-Test POST: 
   Go to http://127.0.0, click your route, and use the "Try it out" button.
   Python console
   Bash

More on FastAPI
- generate OpenAI standard schema with all your API which powered interactive /docs
- path define route / endpoint of request
- support all HTTP method
- built on python type hint: enable type declaration of variable (data validation etc.)
*********************

requests module
- allow you to send HTTP requests using Python.
- The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
- available methods (excerpt)
    post(url, data, json, args) : Sends a POST request to the specified url. data: data to send
    get(url, params, args)
    request(method, url, args) : Sends a request of the specified method to the specified url
    eg  response = requests.post(url, json=data)
        response = requests.get(url)
- handling http requests error   using  
    requests.exceptions.HTTPError as error  : display 404 / 300 etc. response.raise_for_status() method
    requests.exceptions.TooManyRedirects : 3xx error   response.raise_for_status() method
    requests.ConnectionError  :  when not receive a response from the server
    requests.Timeout :  API server accepts your connection but cannot finish request within the allowed time
    
   
LOGGING MODULE
- level of logging
    Debug (10): Useful for diagnosing issues in the code.
    Info (20): It can act as an acknowledgment that there are no bugs in the code. One good use-case of Info level logging is the progress of training a machine learning model.
    Warning (30): Indicative of a problem that could occur in the future. For example, a warning of a module that might be discontinued in the future or low-ram warning.
    Error (40): A serious bug in the code, could be a syntax error, out of memory error, exceptions.
    Critical (50): An error due to which the program might stop functioning or might exit abruptly.
- by default, only severity above 20 will be logged. 
   can edit using logging.basicConfig(level=logging.INFO)  : so 20 & above will be logged
-example logging format setting using basicConfig method (optional)
    logging.basicConfig(
      level=logging.INFO,
         format=( "%(asctime)s - %(levelname)s - %(message)s" ))
- available attributes
   %(asctime)s : human readable time
   %(levelname)s : logging level in text
   %(levelno)s : logging level in no
   %(message)s  : logged message
   %(funcName)s : function containing the logging call
-logging.error("An Error Logging Message")  : create log with error severity
- -logging.basicConfig(level = logging.INFO, filename = 'datacamp.log')
 : set INFO and above will be logged into file(appended by default)
- logging.basicConfig(level = logging.INFO, filename = 'datacamp.log', filemode = 'w')
   ; logged are overwritten everytime (def is 'a' append)
