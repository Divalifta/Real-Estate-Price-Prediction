from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': ['Rajaji Nagar', 'Electronic City', 'Koramangala', 'Whitefield', 'Other Location 1',
                      'Other Location 2']
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()  # Expecting JSON data

        # Check if required data is provided
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        BHK = int(data.get('BHK', 0))
        bath = int(data.get('bath', 0))

        # Validate data
        if not location or total_sqft <= 0 or BHK <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid or missing data'}), 400

        # Predict the price
        estimated_price = util.get_estimated_price(location, total_sqft, BHK, bath)

        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)


