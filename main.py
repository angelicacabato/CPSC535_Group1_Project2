

# importing other python files for data process and algorithm implementation
from flask import Flask, request, jsonify, render_template, render_template, url_for
from floyd_warshall import floyd_warshall
from process_map_data import process_map_data

app = Flask(__name__)

cafeLocations = {}
blockages = []

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/about')
def about():
    return render_template('about.html')  
    

@app.route('/calculate_path', methods=['POST'])
def calculate_path():
    data = request.get_json()  # Access the JSON data sent with the request   
    try:
        # Use source and destination names to lookup their respective coordinates
        path = process_map_data(source_location=cafeLocations.get(data['source']), 
                                destination_location=cafeLocations.get(data['destination']),
                                blockages=blockages, cafeLocations=cafeLocations)
        return jsonify({'path': path})
    except Exception as e:
        print(f"Error processing path: {e}")
        return jsonify({'error': 'Failed to calculate path'}), 500

@app.route('/get_cafes', methods=['GET'])
def get_cafes():
    global cafeLocations
    _, cafe_list = process_map_data(fetch_cafes_only=True, blockages=blockages, cafeLocations=cafeLocations)
    # Populate cafeLocations with the fetched cafes
    cafeLocations = {cafe['name']: (cafe['lat'], cafe['lng']) for cafe in cafe_list}
    return jsonify({'cafes': cafe_list})

@app.route('/report_blockage', methods=['POST']) # New endpoint to handle blockage reporting
def report_blockage():
    data = request.get_json()
    new_blockage = (data['source'], data['destination'])
    if new_blockage not in blockages:
        blockages.append(new_blockage)
    return jsonify({'message': 'Blockage reported successfully, calculating new route for you.'}), 200


def main():

    process_map_data()


if __name__ == "__main__":
    app.run(debug=True)
    main()

