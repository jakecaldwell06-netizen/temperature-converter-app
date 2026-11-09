# Temperature Converter App

My first Streamlit app - converts temperatures between Celsius and Fahrenheit.

Built for FINAN 623 (Building Apps with AI, Streamlit, and GitHub).

## Features
- Enter any temperature (decimals and negatives allowed)
- Choose Celsius → Fahrenheit or Fahrenheit → Celsius
- See the converted temperature
- See the formula used, with your numbers plugged in
- Friendly error messages for blank, text, or symbol input
- Warning for temperatures below absolute zero

## Formulas
- Celsius to Fahrenheit: F = (C × 9/5) + 32
- Fahrenheit to Celsius: C = (F − 32) × 5/9

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
