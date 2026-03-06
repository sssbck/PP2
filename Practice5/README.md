# Practice 5 – Python Regular Expressions (RegEx)

## Overview

The purpose of this practice is to study and apply Python Regular Expressions using the `re` module. The exercises include working with pattern matching, searching, splitting, and replacing text using regex. A practical task involves parsing receipt data from a raw text file.

## Implemented Tasks

* Studied the fundamentals of Python Regular Expressions based on the W3Schools tutorial
* Practiced creating and testing regex patterns
* Implemented examples using the following functions:

  * `re.search()`
  * `re.findall()`
  * `re.split()`
  * `re.sub()`
* Implemented a receipt parser to extract structured information from `raw.txt`

## Extracted Information

The parser extracts the following data from the receipt:

* Product names
* Product prices
* Total amount
* Date and time of purchase
* Payment method

The extracted information is displayed in JSON format.

## Project Structure

Practice5/
│
├── receipt_parser.py
├── raw.txt
└── README.md

## Execution

To run the program:

bash id="runparser01"
python receipt_parser.py

## Technologies Used

* Python
* Regular Expressions (`re` module)
* JSON
