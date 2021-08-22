# JSON Savings
JSON Savings is a tool that allows you to calculate potential savings in your cloud bandwidth bill.

## Demo
- https://json-savings.herokuapp.com/ (it might take a couple seconds to start sometimes; it's hosted for free on heroku).

## How do we do it?
We compare joint encoding and compression techniques against each other. We use Python and the python versions of the techniques to perform the calculation. We also use streamlit to put thing neatly into a presentable interface.

### Encoding Techniques

- msgpack
- cbor

### Compression Techniques

- brotli
- zstd
- snappy
- gz

## Want to run it locally?

- Clone the repository
- run `pip install -r requirements.txt`
- run `streamlit run app.py`, and the app should open in your browser

## Contribution

Feel free to contribute to fix any bugs or add new algorithms and techniques to the mix.
