# =============================================================================
# Temperature Converter App
# FINAN 623 - Building Apps with AI, Streamlit, and GitHub
#
# What this app does:
#   1. Lets the user type in a temperature value
#   2. Lets the user pick a conversion type (C -> F or F -> C)
#   3. Shows the converted temperature
#   4. Shows the formula that was used, with the user's numbers plugged in
#   5. Uses a clean, simple layout
#
# How to run it on your own computer:
#   pip install streamlit
#   streamlit run app.py
# =============================================================================

# -----------------------------------------------------------------------------
# SECTION 1: Imports
# streamlit builds the web page. math is part of Python itself (no install
# needed) and is only used to catch values like "inf" or "nan".
# -----------------------------------------------------------------------------
import math

import streamlit as st


# -----------------------------------------------------------------------------
# SECTION 2: Page setup
# This must be the first Streamlit command. It sets the browser tab title,
# the little icon on the tab, and keeps the layout narrow and centered.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Temperature Converter",
    page_icon="🌡️",
    layout="centered",
)


# -----------------------------------------------------------------------------
# SECTION 3: Constants
# Absolute zero is the coldest possible temperature. Anything below it is not
# physically possible, so the app warns the user (but still does the math).
# -----------------------------------------------------------------------------
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67


# -----------------------------------------------------------------------------
# SECTION 4: Conversion functions
# Each function does ONE job: take a number in, return the converted number.
# Keeping the math in its own function makes it easy to check and test.
#
#   Celsius to Fahrenheit:  F = (C x 9/5) + 32
#   Fahrenheit to Celsius:  C = (F - 32) x 5/9
# -----------------------------------------------------------------------------
def celsius_to_fahrenheit(celsius):
    """Convert a Celsius temperature to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert a Fahrenheit temperature to Celsius."""
    return (fahrenheit - 32) * 5 / 9


# -----------------------------------------------------------------------------
# SECTION 5: Input checking (error handling)
# The user types into a text box, so they could type anything: "hello",
# "!@#$", or nothing at all. This function tries to turn the text into a
# number. If it can't, it returns an error message instead of crashing.
#
# It returns two things: (number, error_message)
#   - Good input  -> (98.6, None)
#   - Bad input   -> (None, "some message explaining the problem")
# -----------------------------------------------------------------------------
def parse_temperature(text):
    """Turn the user's text into a number, or explain why it can't be."""
    cleaned = text.strip().replace(",", "")  # allow "1,000,000"

    # Empty input
    if cleaned == "":
        return None, "Please enter a temperature value."

    # Try to convert the text to a decimal number
    try:
        value = float(cleaned)
    except ValueError:
        return None, (
            f'"{text.strip()}" is not a number. '
            "Please enter digits only, like 25, -40, or 98.6."
        )

    # Python's float() accepts words like "inf" and "nan" - block those
    if not math.isfinite(value):
        return None, "Please enter a real, finite number."

    return value, None


# -----------------------------------------------------------------------------
# SECTION 6: Number formatting
# Shows up to 2 decimal places, drops trailing zeros (32.00 -> 32), and adds
# commas to big numbers (1800032 -> 1,800,032).
# -----------------------------------------------------------------------------
def format_number(value):
    """Format a number for display."""
    rounded = round(value, 2)
    if rounded == 0:
        rounded = 0.0  # avoid showing "-0"
    text = f"{rounded:,.2f}".rstrip("0").rstrip(".")
    return text


# -----------------------------------------------------------------------------
# SECTION 7: Page header and instructions
# -----------------------------------------------------------------------------
st.title("🌡️ Temperature Converter")
st.write("Convert temperatures between **Celsius** and **Fahrenheit**.")

with st.expander("How to use this app"):
    st.markdown(
        """
        1. Choose which way you want to convert.
        2. Type a temperature in the box (decimals and negatives are fine).
        3. Press **Enter** or click **Convert**.
        4. Your answer and the formula used will appear below.
        """
    )


# -----------------------------------------------------------------------------
# SECTION 8: User inputs
# A form groups the inputs with a Convert button. Pressing Enter in the text
# box also submits the form.
# -----------------------------------------------------------------------------
with st.form("converter_form"):
    # Conversion type: two choices shown side by side
    conversion = st.radio(
        "Conversion type",
        options=["Celsius → Fahrenheit", "Fahrenheit → Celsius"],
        horizontal=True,
    )

    # Text box (not a number box) so the app can show a friendly error
    # message when someone types letters, symbols, or nothing at all
    temperature_text = st.text_input(
        "Temperature to convert",
        placeholder="e.g. 25, -40, or 98.6",
    )

    submitted = st.form_submit_button("Convert", type="primary")


# -----------------------------------------------------------------------------
# SECTION 9: Do the conversion and show the results
# This only runs after the user clicks Convert (or presses Enter).
# -----------------------------------------------------------------------------
if submitted:
    value, error = parse_temperature(temperature_text)

    # Bad input: show the error and stop here
    if error:
        st.error(error)

    # Good input: convert, then show result + formula
    else:
        if conversion == "Celsius → Fahrenheit":
            result = celsius_to_fahrenheit(value)
            in_unit, out_unit = "°C", "°F"
            formula = "F = (C × 9/5) + 32"
            worked = f"F = ({format_number(value)} × 9/5) + 32 = {format_number(result)}"
            below_absolute_zero = value < ABSOLUTE_ZERO_C
        else:
            result = fahrenheit_to_celsius(value)
            in_unit, out_unit = "°F", "°C"
            formula = "C = (F − 32) × 5/9"
            worked = f"C = ({format_number(value)} − 32) × 5/9 = {format_number(result)}"
            below_absolute_zero = value < ABSOLUTE_ZERO_F

        # Main answer, shown large
        st.success(
            f"**{format_number(value)} {in_unit} = {format_number(result)} {out_unit}**"
        )

        # Side-by-side input and output boxes
        col1, col2 = st.columns(2)
        col1.metric("You entered", f"{format_number(value)} {in_unit}")
        col2.metric("Converted", f"{format_number(result)} {out_unit}")

        # The formula, both general and with the user's numbers plugged in
        st.subheader("Formula used")
        st.code(formula, language=None)
        st.code(worked, language=None)

        # Physics check: warn if below absolute zero
        if below_absolute_zero:
            st.warning(
                f"Heads up: {format_number(value)} {in_unit} is below absolute "
                f"zero ({format_number(ABSOLUTE_ZERO_C)} °C / "
                f"{format_number(ABSOLUTE_ZERO_F)} °F), the coldest temperature "
                "that is physically possible. The math above is still correct."
            )


# -----------------------------------------------------------------------------
# SECTION 10: Quick reference table (always visible at the bottom)
# Handy known values the user can use to check the app is right.
# -----------------------------------------------------------------------------
st.divider()
st.caption("Quick reference")
st.markdown(
    """
    | Celsius | Fahrenheit | What it is |
    |---:|---:|---|
    | −40 °C | −40 °F | Where the two scales meet |
    | 0 °C | 32 °F | Water freezes |
    | 37 °C | 98.6 °F | Normal body temperature |
    | 100 °C | 212 °F | Water boils |
    """
)
