from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

# Replace with your Facebook app's credentials
FB_APP_ID = 'YOUR_APP_ID'
FB_APP_SECRET = 'YOUR_APP_SECRET'
FB_REDIRECT_URI = 'http://127.0.0.1:5000/login/callback'


@app.route('/')
def home():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Name Changer</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #f0f2f5;
                }
                .btn {
                    padding: 10px;
                    background-color: #4267B2;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>

        <h1>Login to Change Your Facebook Name</h1>
        <a href="{{ url_for('login') }}">
            <button class="btn">Login with Facebook</button>
        </a>

        </body>
        </html>
        """
    )


@app.route('/login')
def login():
    return redirect(
        f'https://www.facebook.com/v15.0/dialog/oauth?client_id={FB_APP_ID}&redirect_uri={FB_REDIRECT_URI}&scope=public_profile,email'
    )


@app.route('/login/callback')
def login_callback():
    # Facebook returns a code, which we can use to get the access token
    code = request.args.get('code')
    token_url = f'https://graph.facebook.com/v15.0/oauth/access_token?client_id={FB_APP_ID}&redirect_uri={FB_REDIRECT_URI}&client_secret={FB_APP_SECRET}&code={code}'

    # Request access token from Facebook
    response = requests.get(token_url)
    access_token = response.json().get('access_token')

    # Get user profile data
    user_data = requests.get(f'https://graph.facebook.com/me?access_token={access_token}&fields=name,email').json()

    # Store user data
    user_name = user_data['name']
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Update Your Name</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f2f5;
                    text-align: center;
                }
                .form-container {
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    width: 300px;
                    margin: 0 auto;
                }
                .input-field {
                    padding: 10px;
                    margin: 10px 0;
                    width: 100%;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }
                .submit-btn {
                    padding: 10px;
                    background-color: #4267B2;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>

        <h1>Update Your Name</h1>

        <p>Your current name is: {{ user_name }}</p>

        <div class="form-container">
            <form method="POST" action="{{ url_for('update_name') }}">
                <input class="input-field" type="text" name="fast_name" placeholder="Fast Name" required>
                <input class="input-field" type="text" name="second_name" placeholder="2nd Name" required>
                <input class="input-field" type="text" name="third_name" placeholder="3rd Name" required>
                <input class="input-field" type="text" name="emoji_name" placeholder="Add Emoji" required>
                <button type="submit" class="submit-btn">Update Name</button>
            </form>
        </div>

        </body>
        </html>
        """, user_name=user_name)


@app.route('/update_name', methods=['POST'])
def update_name():
    fast_name = request.form['fast_name']
    second_name = request.form['second_name']
    third_name = request.form['third_name']
    emoji_name = request.form['emoji_name']

    # Combine the names and emoji
    new_name = f"{fast_name} {second_name} {third_name} {emoji_name}"

    # Assuming you have the access token (you would retrieve this in the login callback):
    access_token = 'USER_ACCESS_TOKEN'  # Replace with actual access token
    fb_api_url = f'https://graph.facebook.com/v15.0/me?access_token={access_token}'

    # Update the Facebook profile with the new name
    response = requests.post(fb_api_url, data={'name': new_name})
    if response.status_code == 200:
        return f'Your name has been updated to {new_name}!'
    else:
        return 'There was an error updating your name.'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
