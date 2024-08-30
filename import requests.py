import requests

def get_instagram_conversations(instagram_account_id, access_token):
    url = f"https://graph.facebook.com/v20.0/{instagram_account_id}/conversations"
    params = {
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        conversations = response.json()
        return conversations
    else:
        print(f"Error: Unable to fetch conversations. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Replace these variables with your actual Instagram Account ID and Access Token
INSTAGRAM_ACCOUNT_ID = '17841405338225722'
ACCESS_TOKEN = 'EAAYZAd4mw7WQBOZC5svU1hqmdhAh2HqWlgQvAPujihP50nmDMGe9VU2UDiZAI8lWujbnxFsA0MkFlWkunbFILXXd0by6pp3e58KklbjTZCFkTRumQ1aLbG1IYXNoii54ZCbBymeFJfyNGOGLI3vqZCqLzOwizXi6LLr9qXETwZCfuDf3CGK4MMcZBoyZAZBo8evIh9u0bs7TtUClUoI6IjfkPkZCGCYZC2C7'

conversations = get_instagram_conversations(INSTAGRAM_ACCOUNT_ID, ACCESS_TOKEN)

if conversations:
    print("Conversations retrieved successfully:")
    print(conversations)
else:
    print("No conversations found or an error occurred.")
