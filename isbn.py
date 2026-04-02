from flask import Flask, jsonify

app  =  Flask(__name__)

# ISBN LOGIC

def strip(isbn):
    return isbn.replace("-","").replace(" ","")

def isbn10_check_digit(isbn9):
    isbn9 = strip(isbn9)
    if len(isbn9) != 9 or not isbn9.isdigit():
        raise ValueError("Input must be exactly 9 digits.")
    total = sum((i+1) * int(d) for i, d in enumerate(isbn9))
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)

def isbn10_validate(isbn):
    isbn = strip(isbn)
    if len(isbn) != 10:
        return False
    if not isbn[:9].isdigit():
        return False
    if isbn[9] not in "0123456789X":
        return False
    total = sum((i+1) * (10 if d == "X" else int(d)) for i, d in enumerate(isbn))
    return total % 11 == 0
    
def isbn10_to_isbn13(isbn10):
    isbn10 = strip(isbn10)
    if not isbn10_validate(isbn10):
        raise ValueError("Invalid ISBN-10; cannot convert.")
    body12 = "978" + isbn10[:9]
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(body12))
    check = (10 - (total % 10)) % 10
    return body12 + str(check)
    
def isbn13_validate(isbn13):
    isbn = strip(isbn)
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(isbn))
    return total % 10 == 0   
    
# API ROUTE

@app.route("/")
def index():
    return jsonify({
        "endpoints": [
            "GET /isbn10/check-digit/<isbn9>  → compute check digit",
            "GET /isbn10/validate/<isbn10>    → validate ISBN-10",
            "GET /isbn10/to-isbn13/<isbn10>   → convert to ISBN-13",
            "GET /isbn13/validate/<isbn13>    → validate ISBN-13",
        ]
    })


@app.route("/isbn10/check-digit/<isbn9>")
def api_check_digit(isbn9):
    try:
        check = isbn10_check_digit(isbn9)
        return jsonify({"isbn9": strip(isbn9), "check_digit": check, "isbn10": strip(isbn9) + check})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/isbn10/validate/<isbn10>")
def api_isbn10_validate(isbn10):
    valid = isbn10_validate(isbn10)
    return jsonify({"isbn10": strip(isbn10), "valid": valid})


@app.route("/isbn10/to-isbn13/<isbn10>")
def api_to_isbn13(isbn10):
    try:
        isbn13 = isbn10_to_isbn13(isbn10)
        return jsonify({"isbn10": strip(isbn10), "isbn13": isbn13})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/isbn13/validate/<isbn13>")
def api_isbn13_validate(isbn13):
    valid = isbn13_validate(isbn13)
    return jsonify({"isbn13": strip(isbn13), "valid": valid})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

        
    
    
    