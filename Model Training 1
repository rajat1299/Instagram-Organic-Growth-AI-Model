import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the preprocessed DataFrame
df = pd.read_csv('preprocessed_data.csv')

# Feature Engineering
# Create new features based on identified potential features
df['Posts_to_Followers_Ratio'] = df['Posts'] / df['Followers']
df['Likes_to_Followers_Ratio'] = df['Avg__Likes'] / df['Followers']
df['Engagement_Rate'] = df['Avg__Likes'] / df['Followers']

# Prepare the features and target variable
features = [
    'Posts', 'Followers', 'Avg__Likes', 'Eng_Rate',
    'Posts_to_Followers_Ratio', 'Likes_to_Followers_Ratio', 'Engagement_Rate',
    'Category_Beauty_&_Makeup', 'Category_Craft/DIY', 'Category_Health,_Sports_&_Fitness',
    'Category_Lifestyle', 'Category_News_&_Politics', 'Category_entertainment',
    'Category_fashion', 'Category_food', 'Category_photography', 'Category_technology'
]
target = 'Engagement_Rate'  # Assuming engagement rate as the target variable

# Split the data into training and testing sets
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the numerical features
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the AI model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Refine the model
# Adjust hyperparameters, try different algorithms, or incorporate additional features
# Example: Trying a different algorithm (e.g., Random Forest Regression)
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

rf_y_pred = rf_model.predict(X_test_scaled)
rf_mse = mean_squared_error(y_test, rf_y_pred)
rf_r2 = r2_score(y_test, rf_y_pred)
print(f"Random Forest - Mean Squared Error: {rf_mse}")
print(f"Random Forest - R-squared: {rf_r2}")
