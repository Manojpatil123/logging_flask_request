import logging
from flask import Flask, request, jsonify
from time import strftime
import traceback
from logging.handlers import RotatingFileHandler

output={}
input={}
app = Flask(__name__)


@app.route('/')
def ap1i():
    return "Happy !"
# API endpoint
@app.route('/api', methods=['post'])
def api():
    name = request.form.get('name')
    age = request.form.get('age')

    if int(age)>25:
        value='yes'
    else:
        value='no'
    input['name']=name
    input['age']=age
    output['output_name']=value
        
    return jsonify(value)

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status,
                      input,
                      output
                      )
    return response   

@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s ERROR MESSAGE\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  e)
    return "Internal Server Error", 500

if __name__ == '__main__':
    handler = RotatingFileHandler('logs.log', maxBytes=10000, backupCount=3)        
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    app.run()