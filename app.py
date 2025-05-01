
import random
import string
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated gift card database
CARD_TYPES = ["Amazon", "Xbox", "PayPal", "Roblox", "Fortnite", "Steam", "iTunes", "GooglePlay"]
DATA_FILE = "codes.json"

# Load existing codes or initialize empty structure
try:
    with open(DATA_FILE, "r") as f:
        card_db = json.load(f)
except FileNotFoundError:
    card_db = {card_type: [] for card_type in CARD_TYPES}

# Save codes to file
def save_db():
    with open(DATA_FILE, "w") as f:
        json.dump(card_db, f, indent=2)

# Generate a fake card code
def generate_code(length=16):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    card_type = data.get("card_type")
    quantity = int(data.get("quantity", 1))

    if card_type not in CARD_TYPES:
        return jsonify({"error": "Invalid card type."}), 400

    new_codes = []
    for _ in range(quantity):
        code = generate_code()
        card_db[card_type].append({"code": code, "redeemed": False})
        new_codes.append(code)

    save_db()
    return jsonify({"generated": new_codes})

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    card_type = data.get("card_type")
    code = data.get("code")

    if card_type not in CARD_TYPES:
        return jsonify({"error": "Invalid card type."}), 400

    for entry in card_db[card_type]:
        if entry["code"] == code:
            return jsonify({"valid": True, "redeemed": entry["redeemed"]})

    return jsonify({"valid": False})

@app.route("/redeem", methods=["POST"])
def redeem():
    data = request.json
    card_type = data.get("card_type")
    code = data.get("code")

    if card_type not in CARD_TYPES:
        return jsonify({"error": "Invalid card type."}), 400

    for entry in card_db[card_type]:
        if entry["code"] == code:
            if entry["redeemed"]:
                return jsonify({"success": False, "message": "Code already redeemed."})
            else:
                entry["redeemed"] = True
                save_db()
                return jsonify({"success": True, "message": "Code redeemed."})

    return jsonify({"success": False, "message": "Code not found."})

if __name__ == "__main__":
    app.run(debug=True)
