import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
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
target = 'Engagement_Rate'

X = df[features]
y = df[target]

# Scale the numerical features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Perform cross-validation
cv_scores_lr = cross_val_score(LinearRegression(), X_scaled, y, cv=5, scoring='r2')
cv_scores_rf = cross_val_score(RandomForestRegressor(n_estimators=100, random_state=42), X_scaled, y, cv=5, scoring='r2')

print("Linear Regression - Cross-validation R-squared scores:", cv_scores_lr)
print("Linear Regression - Mean R-squared score:", cv_scores_lr.mean())
print("Random Forest - Cross-validation R-squared scores:", cv_scores_rf)
print("Random Forest - Mean R-squared score:", cv_scores_rf.mean())

# Train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_scaled, y)

# Get feature importance scores
importances = rf_model.feature_importances_
feature_importances = pd.Series(importances, index=features).sort_values(ascending=False)

print("Feature importances:")
print(feature_importances)
