from flask import Flask, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/kidney-stone/predict', methods=['GET'])
def predict():
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
        df_new = pd.DataFrame([data_list])

        # Load the saved model
        loaded_model = pickle.load(open('naive_bayes_model.sav', 'rb'))

        # Predict the probability
        return str(loaded_model.predict_proba(df_new)[0][0])

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()