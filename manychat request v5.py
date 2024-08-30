from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Function to initialize the SQLite database and table
def init_db():
    conn = sqlite3.connect('giveaway_codes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT,
            user_id TEXT,
            page_id TEXT,
            status TEXT,
            first_name TEXT,
            last_name TEXT,
            name TEXT,
            gender TEXT,
            profile_pic TEXT,
            locale TEXT,
            language TEXT,
            timezone TEXT,
            live_chat_url TEXT,
            last_input_text TEXT,
            optin_phone BOOLEAN,
            phone TEXT,
            optin_email BOOLEAN,
            email TEXT,
            subscribed TEXT,
            last_interaction TEXT,
            ig_last_interaction TEXT,
            last_seen TEXT,
            ig_last_seen TEXT,
            is_followup_enabled BOOLEAN,
            ig_username TEXT,
            ig_id TEXT,
            whatsapp_phone TEXT,
            optin_whatsapp BOOLEAN,
            phone_country_code TEXT,
            last_growth_tool TEXT,
            custom_fields TEXT,
            detected_code TEXT
        )
    ''')
    cursor.execute("PRAGMA table_info(responses)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'detected_code' not in columns:
        cursor.execute('ALTER TABLE responses ADD COLUMN detected_code TEXT')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(data):
    conn = sqlite3.connect('giveaway_codes.db')
    cursor = conn.cursor()
    last_input_text = data.get('last_input_text', '')
    detected_code = None
    match = re.search(r'\bFDR-[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{5}\b', last_input_text, re.IGNORECASE)
    if match:
        detected_code = match.group(0)
    cursor.execute('''
        INSERT INTO responses (
            key, user_id, page_id, status, first_name, last_name, name, gender,
            profile_pic, locale, language, timezone, live_chat_url, last_input_text,
            optin_phone, phone, optin_email, email, subscribed, last_interaction,
            ig_last_interaction, last_seen, ig_last_seen, is_followup_enabled,
            ig_username, ig_id, whatsapp_phone, optin_whatsapp, phone_country_code,
            last_growth_tool, custom_fields, detected_code
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('key'),
        data.get('id'),
        data.get('page_id'),
        data.get('status'),
        data.get('first_name'),
        data.get('last_name'),
        data.get('name'),
        data.get('gender'),
        data.get('profile_pic'),
        data.get('locale'),
        data.get('language'),
        data.get('timezone'),
        data.get('live_chat_url'),
        last_input_text,
        data.get('optin_phone'),
        data.get('phone'),
        data.get('optin_email'),
        data.get('email'),
        data.get('subscribed'),
        data.get('last_interaction'),
        data.get('ig_last_interaction'),
        data.get('last_seen'),
        data.get('ig_last_seen'),
        data.get('is_followup_enabled'),
        data.get('ig_username'),
        data.get('ig_id'),
        data.get('whatsapp_phone'),
        data.get('optin_whatsapp'),
        data.get('phone_country_code'),
        data.get('last_growth_tool'),
        str(data.get('custom_fields', {})),
        detected_code
    ))
    conn.commit()
    conn.close()

@app.route('/your-endpoint', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    
    init_db()
    insert_data(data)
    
    detected_code = None
    if 'last_input_text' in data:
        match = re.search(r'\bFDR-[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{5}\b', data['last_input_text'], re.IGNORECASE)
        if match:
            detected_code = match.group(0)
    
    if detected_code:
        response = {
            "code_response": f"""Congratulations! 🎉 You've been entered in our first giveaway!

Want to up your chances of winning and join the official A$AP Defense Squad? Simply follow the link below to join our Official Discord, and use your unique code to become 'Defense Squad' official.

Here’s your Defense Squad code: {detected_code}

Discord link: https://bit.ly/46RiUjy

We can't wait to see you on the inside!"""
        }
    else:
        response = {
            "code_response": "No code detected, please try again."
        }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
