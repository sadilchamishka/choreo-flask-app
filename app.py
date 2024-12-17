from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

books = []

# helper function to generate IDs
def generate_id():
    return len(books) + 1

@app.route('/reading-list/predict')
def predict():
    return 'Hello World'

# endpoint to get all books
@app.route('/reading-list/books', methods=['GET'])
def get_books():
    try:
        # List of expected parameters
        params = ['param1', 'param2', 'param3', 'param4', 'param5', 'param6']

        # Fetching parameters from request and validating if they are present
        data_list = []
        for param in params:
            value = request.args.get(param)
            if value is None:
                return f"Error: Missing query parameter '{param}'"
            try:
                data_list.append(float(value))
            except ValueError:
                return f"Error: Query parameter '{param}' must be a valid number"

        # Reshaping the list to match the expected input format
        #df_new = pd.DataFrame([data_list])

        # Load the saved model
        loaded_model = pickle.load(open('naive_bayes_model.sav', 'rb'))

        # Predict the probability
        #return str(loaded_model.predict_proba(df_new)[0][0])

    except Exception as e:
        return f"Error: {str(e)}"


# endpoint to add a new book
@app.route('/reading-list/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = {
        'id': generate_id(),
        'author': data['author'],
        'name': data['name'],
        'status': data['status']
    }
    books.append(book)
    return jsonify(book)

# endpoint to get a book by ID
@app.route('/reading-list/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return '', 404

# endpoint to delete a book by ID
@app.route('/reading-list/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return '', 204

# endpoint to update a book status by ID
@app.route('/reading-list/books/<int:book_id>', methods=['PUT'])
def update_book_status(book_id):
    data = request.get_json()
    for book in books:
        if book['id'] == book_id:
            book['status'] = data['status']
            return jsonify(book)
    return '', 404

if __name__ == '__main__':
    app.run()