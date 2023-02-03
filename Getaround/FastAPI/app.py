import uvicorn
from fastapi import FastAPI
import pandas as pd 
from pydantic import BaseModel
from typing import Union
import joblib
import json



# description will apear in the doc
description = """
Getaround pricing API   
"""

# tags to identify different endpoints                              ### NOTE_ : Definition de l"URL /preview
tags_metadata = [
    {
        "name": "Preview",
        "description": "Preview the random rows",
    },

    {
        "name": "Model-Prediction",
        "description": "Estimate rental price based on machine learning model"
    }
]

app = FastAPI(
    title="🔑 Getaround API 🚗",
    description=description,
    version="1.0",
    contact={
        "name": "Hello, check out my github to learn more about my project.",
        "url": "https://github.com/DanyNgn",                               
    },
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/", tags=["Preview"])
async def random_data(rows: int= 3):
    """
    Get a sample of your whole dataset.   
    You can specify amount of rows that you want by specifying a value for `rows`, default is `3`.
    """
    try:
        if rows < 51 :
            fname ="get_around_pricing-project_copy.csv"
            df = pd.read_csv(fname)
            sample = df.sample(rows)
            response0= sample.to_json(orient='records')
        else:
            response0 = json.dumps({"message" : "Error! Row number should not be more than 50."})
    except:
            response0 = json.dumps({"message" : "Error! Problem."})


@app.post("/predict", tags=["Model-Prediction"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction for single set of input variables. Possible input values are:  
    model_key: str  
    mileage: float  
    engine_power: float  
    fuel: str  
    paint_color: str  
    car_type: str  
    private_parking_available: bool  
    has_gps: bool  
    has_air_conditioning: bool  
    automatic_car: bool  
    has_getaround_connect: bool  
    has_speed_regulator: bool  
    winter_tires: bool  
    Endpoint returns a dictionnary in the following format:  
    ```
    {'prediction': rental_price_per_day}  
    ```
    You need to use values as a dictionnary, or a form data.  
    """
    if predictionFeatures.json :  
      # Printing JSON as dictionnary for user to check variables
        print(predictionFeatures)
        # Read data 
        df = pd.DataFrame(dict(predictionFeatures), index=[0])

        # Load the models from local
        # prepro_getaround = 'prepro.joblib' # preprocessing model - *_* pas besoin de prepro
        model_getaround  = 'model.joblib' # Linear regression

        # preprocess = joblib.load(prepro_getaround) # *_* pas besoin de prepro
        regressor = joblib.load(model_getaround)
        
        try: 
            # X_val = preprocess.transform(df.head(16)) # *_* pas besoin de prepro
            Y_pred = regressor.predict(df)
            print(Y_pred)
            # Prediction
            # Format response
            response = {'Predicted rental price per day in dollars': round(Y_pred.tolist()[0],1)}
        except:
            response = json.dumps({"message" : """Error! Check your input format."""})
        return response
    else:
        msg = json.dumps({"message" : """Error! Check your input format."""})
        return msg

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 4000, debug=True, reload=True)