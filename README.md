# QR _2_ Text

Little fun tool to turn your __boring QR-code images__ into __funny Unicode text__ that looks exactly the same!

## Why this exists

I really wanted some tool to write QR codes in the places they are not meant to be. 
So I created a script for that, and now you can do cool-looking things like this:
<p align="center">
<img src="examples/usage_example.png" alt="Usage example image" height="300"/>
</p>

## Getting started

1) Clone or download repository
2) You must have python3 installed to use qr2text, so install it if you haven't already
3) Enter the repository directory
4) Install the required python packages with 
`pip3 install -r requirements.txt`

Now you can finally run program!

## How to use

### Usage:
`$ python3 qr2text.py [Image-file name]`

Using the script like that will make it use the `[Image-file]` (JPEG / PNG file) as input and console as output.

### Available options:
+ `-h / --help` - will make the program show the script usage guide 
+ `-of / --outputfile [Output text-file name]` - will make the script output the result to a specified file
+ `-i / --inverted` - will invert the colors of the output
+ `-s / --scale [Scale]` - will the scale the `1 x 1` pixel of original QR-code up to `[Scale] x [Scale]` pixels

