from flask import Flask, request, jsonify, make_response
import psycopg2
import re
import time
import random

app = Flask(__name__)

# Database connection details
DB_HOST = "dmbotpublic.clbaspno09lp.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"  # Replace with your database name
DB_USER = "postgres"  # Replace with your PostgreSQL username
DB_PASSWORD = "CloudMicro99!"

# Function to initialize the PostgreSQL database and tables
def init_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Create 'responses' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
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

    # Create 'codes' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id SERIAL PRIMARY KEY,
            code1 TEXT UNIQUE,
            code2 TEXT
        )
    ''')

    # Prepopulate 'codes' table with some codes if it's empty
    cursor.execute('SELECT COUNT(*) FROM codes')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO codes (code1, code2) VALUES (%s, %s)
        ''', [
            ('FDR-ABC12345', 'GHI67890'),
            ('FDR-DEF23456', 'JKL78901'),
            ('FDR-GHI34567', 'MNO89012')
        ])

    conn.commit()
    cursor.close()
    conn.close()

# Function to insert data into the 'responses' table
def insert_data(data):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
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
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    cursor.close()
    conn.close()

# Function to check detected code against the 'codes' table
def check_code(detected_code):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute('SELECT code2 FROM codes WHERE code1 = %s', (detected_code.upper(),))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

@app.route('/your-endpoint', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    
    last_input_text = data.get('last_input_text', '')
    
    # Check for the presence of "FDR-"
    detected_code = None
    match = re.search(r'\bFDR-[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{1}[a-zA-Z0-9]{5}\b', last_input_text, re.IGNORECASE)
    if match:
        detected_code = match.group(0)
    
    # If "FDR-" is detected, process the request
    if detected_code:
        insert_data(data)
        code2 = check_code(detected_code)
        
        # Introduce a random delay to simulate human-like behavior
        time.sleep(random.uniform(2, 5))  # Delay between 2 and 5 seconds
        
        if code2:
            response = {
                "code_response": f"""Congratulations! 🎉 You've been entered in our first giveaway!

Want to up your chances of winning and join the official A$AP Defense Squad? Simply follow the link below to join our Official Discord, and use your unique code to become 'Defense Squad' official.

Here’s your Defense Squad code: {code2}

Discord link: https://bit.ly/46RiUjy

We can't wait to see you on the inside!"""
            }
        else:
            response = {
                "code_response": "No matching code found, please try again."
            }
        return jsonify(response), 200
    
    # If no "FDR-" is found, do nothing, return 204 No Content
    return make_response('', 204)

if __name__ == '__main__':
    init_db()  # Initialize the database tables on startup
    app.run(debug=True, port=5000)
