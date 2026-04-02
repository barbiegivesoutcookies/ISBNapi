# SCT-254-011/2023 Emy Ngima Kariuki ISBN API
A simple web API that lets you work with ISBN book numbers. You can check, validate, and convert ISBNs

## What is an ISBN?

An **ISBN** (International Standard Book Number) is a unique number assigned to every published book.

## What the Code Does

The program has two parts:

1. Four simple Python functions that do the actual ISBN math.
2. **API layer** — a Flask web server that exposes those functions as URLs you can call.

### The four functions:

| Function | What it does |
|---|---|
| `isbn10_check_digit` | Given the first 9 digits of an ISBN-10, calculates what the 10th (check) digit should be |
| `isbn10_validate` | Checks whether a full 10-digit ISBN-10 is legitimate |
| `isbn10_to_isbn13` | Converts a valid ISBN-10 into its ISBN-13 equivalent |
| `isbn13_validate` | Checks whether a full 13-digit ISBN-13 is legitimate |

---

## How to Run It

**1. Install the only dependency:**
```bash
pip install flask
```

**2. Start the server:**
```bash
python isbn_api.py
```

**3. The API is now running at:** `http://localhost:5000`

---

## API Endpoints

All endpoints use `GET` requests. Just replace the placeholder with your ISBN number.

Hyphens and spaces in ISBNs are automatically ignored, so `0-19-853453-1` and `0198534531` are treated the same.

---

### (a) Compute the check digit
**`GET /isbn10/check-digit/<first 9 digits>`**

Give it the first 9 digits of an ISBN-10 and it tells you what the check digit should be.

```bash
curl http://localhost:5000/isbn10/check-digit/019853453
```
```json
{
  "isbn9": "019853453",
  "check_digit": "1",
  "isbn10": "0198534531"
}
```

---

### (b) Validate an ISBN-10
**`GET /isbn10/validate/<isbn10>`**

Checks whether a 10-digit ISBN-10 is valid.

```bash
curl http://localhost:5000/isbn10/validate/0198534531
```
```json
{
  "isbn10": "0198534531",
  "valid": true
}
```

---

### (c) Convert ISBN-10 to ISBN-13
**`GET /isbn10/to-isbn13/<isbn10>`**

Converts a valid ISBN-10 into its ISBN-13 equivalent by prepending `978` and recalculating the check digit.

```bash
curl http://localhost:5000/isbn10/to-isbn13/0198534531
```
```json
{
  "isbn10": "0198534531",
  "isbn13": "9780198534532"
}
```

---

### (d) Validate an ISBN-13
**`GET /isbn13/validate/<isbn13>`**

Checks whether a 13-digit ISBN-13 is valid.

```bash
curl http://localhost:5000/isbn13/validate/9780198534532
```
```json
{
  "isbn13": "9780198534532",
  "valid": true
}
```

---

## How the Check Digit Math Works

**ISBN-10:** Multiply each of the 9 digits by its position (1×d1 + 2×d2 + ... + 9×d9), divide by 11, and the remainder is the check digit. If the remainder is 10, the check digit is `X`.

**ISBN-13:** Multiply digits alternately by 1 and 3, sum them up, and the check digit is whatever makes the total divisible by 10.

---

## Error Handling

If you pass invalid input, the API returns an error message and a `400` status code:

```json
{
  "error": "Invalid ISBN-10; cannot convert."
}
```
