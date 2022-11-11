from flask import Flask, jsonify, request
from service import predict

app = Flask(__name__, static_folder='build', static_url_path='/')

@app.route('/')
def index():
	if(request.method == 'GET'):
		return app.send_static_file('index.html')

@app.route('/predict', methods=['GET'])
def help():
	if(request.method == 'GET'):

		symbol = request.args.get('symbol')
		periods = request.args.get('periods')

		if symbol is None:
			symbol = 'MSFT'

		if periods == None:
			periods = '100'

		predication, error = predict(company_symbol=symbol, periods=int(periods))
		print(error)

		result = {"error": error, "predication": predication.to_dict(orient='records')}

		response = jsonify(predication.to_json(orient='records'))
		# response = jsonify(result)
		response.headers.add("Access-Control-Allow-Origin", "*")

		return response

if __name__ == '__main__':
	app.run(debug=True)

