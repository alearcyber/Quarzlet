from flask import Flask, jsonify, request
import json
import os



app = Flask(__name__, root_path='./Authentication/')


credentials = {
    'admin': 'admin',
    'devin': 'patel',
    'vish': 'patel',
    'aidan': 'lear',
    'user': 'pass'
}





################################################################################################
# Authentication
################################################################################################
@app.route('/authenticate', methods=['GET', 'POST'])
def auth():
    # parse arguments
    try:
        content: dict = request.json
        username = content['username']
        password = content['password']
    except:
        print("Auth LOG - could not find JSON or it was not proper JSON formatting.")
        return "ERROR: JSONFormatError - The JSON was not formatted correctly.", 460


    #authenticate
    good = False
    if username in credentials.keys():
        if credentials[username] == password:
            good = True



    #send response
    if good:
        return jsonify({"status": "1"})
    else:
        return jsonify({"status": "0"})




##########################################################################################
# Entry point for the program
##########################################################################################
def main():
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
