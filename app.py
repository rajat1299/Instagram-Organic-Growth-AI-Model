from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load the serialized model and scaler
with open('rf_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame(data, index=[0])
    scaled_data = scaler.transform(df)
    prediction = model.predict(scaled_data)
    return jsonify({'engagement_rate': prediction[0]})

@app.route('/features', methods=['GET'])
def get_features():
    features = [
        'Posts', 'Followers', 'Avg__Likes', 'Eng_Rate',
        'Posts_to_Followers_Ratio', 'Likes_to_Followers_Ratio', 'Engagement_Rate',
        'Category_Beauty_&_Makeup', 'Category_Craft/DIY', 'Category_Health,_Sports_&_Fitness',
        'Category_Lifestyle', 'Category_News_&_Politics', 'Category_entertainment',
        'Category_fashion', 'Category_food', 'Category_photography', 'Category_technology'
    ]
    return jsonify({'features': features})

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = [
        'Beauty_&_Makeup', 'Craft/DIY', 'Health,_Sports_&_Fitness', 'Lifestyle',
        'News_&_Politics', 'entertainment', 'fashion', 'food', 'photography', 'technology'
    ]
    return jsonify({'categories': categories})

@app.route('/retrain', methods=['POST'])
def retrain():
    data = request.json
    df = pd.DataFrame(data)

    # Preprocess the data
    X = df.drop('Engagement_Rate', axis=1)
    y = df['Engagement_Rate']

    # Scale the features
    X_scaled = scaler.fit_transform(X)

    # Retrain the model
    new_model = RandomForestRegressor(n_estimators=100, random_state=42)
    new_model.fit(X_scaled, y)

    # Serialize the retrained model and scaler
    with open('models/rf_model.pkl', 'wb') as file:
        pickle.dump(new_model, file)

    with open('models/scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

    return jsonify({'message': 'Model retrained successfully'})

if __name__ == '__main__':
    app.run(debug=True)
