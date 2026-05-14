# ml/train_model.py

from database.db import get_connection
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


conn = get_connection()

df = pd.read_sql("SELECT * FROM used_cars", conn)

conn.close()



# thing we want the model to predict
y = df["price"] 

# everything the model uses to make the prediction
x = df.drop(columns=["price", "id", "fuel_type", "clean_title", "accident", "engine", "transmission"]) 


# features to encoder
text_features = [ "brand", "model", "ext_col", "int_col" ]
numeric_features = [ "mileage", "year" ]

# encoder is the object that knows how to convert text categories into nurmerical values
encoder = OneHotEncoder(handle_unknown="ignore") 
# ignore prevents crashing if prediction input has a category 
# that the model did not see during training

# column transformer decides which columns/features get the encoder
preprocessor = ColumnTransformer([
    ("text_encoder", encoder, text_features), # pass encoder to text features
    ("numbers", "passthrough", numeric_features) # keep numeric features as numbers
])


# defining training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# steps are the todos for the pipeline
steps = [ 
            ( 'preprocessor', preprocessor ),
            ( 'model', LinearRegression() ),
        ]

model = Pipeline( steps )
model.fit( x_train, y_train ) # fit uses the model in steps to train the model on the training data

# we can predict pricing now through the model
predictions = model.predict( x_test )

# we can also see how many the model can explain
score = model.score(x_test, y_test)
mae = mean_absolute_error(y_test, predictions) 
mae = mae.__round__(2)
# average absolute prediction error in dollars

print(f"Model R^2 Score: {score:.4f}")
print(f"On average, the model was off by ${mae}")




