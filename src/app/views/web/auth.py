import logging
import urllib

import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from app.models.users import UserDetails
from app import utils

logger = logging.getLogger()


def request_oauth_token(request):
    """
    Send the user to the Discord OAuth authorisation page.
    We ask for user identity and list of servers they are in.

    Discord then sends the user back to our auth_callback endpoint, where we process the user.
    """
    base_url = 'https://discord.com/oauth2/authorize?'
    host = request.get_host()
    host = "http://127.0.0.1:5000" if "127.0.0.1" in host else "https://titancraft.cookiehook.com"
    params = {
        'client_id': utils.get_secret('DISCORD_TITANCRAFT_CLIENT_ID'),
        'redirect_uri': host + reverse('auth_callback'),
        'response_type': 'code',
        'scope': 'identify guilds',
        'prompt': 'none'  # Skips auth screen if they've already authorised
    }
    url = base_url + urllib.parse.urlencode(params)
    return redirect(url)


def oauth_callback(request):
    """Process the redirect response sent by Discord"""
    if 'code' not in request.GET:  # Occurs when users cancel Discord authorisation
        logger.info("Login failed. Access code not provided")
        return redirect(reverse('auth_failure'))

    # Trade the short lived code for a discord OAuth token for the authorised user.
    host = request.get_host()
    host = "http://127.0.0.1:5000" if "127.0.0.1" in host else f"https://titancraft.cookiehook.com"
    data = {
        'client_id': utils.get_secret('DISCORD_TITANCRAFT_CLIENT_ID'),
        'client_secret': utils.get_secret('DISCORD_TITANCRAFT_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': request.GET['code'],
        'redirect_uri': host + reverse('auth_callback'),
    }
    token_resp = requests.post('https://discord.com/api/v8/oauth2/token', data=data,
                               headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if token_resp.status_code != 200:
        logger.info(f"Login failed ({token_resp.status_code}) retrieving token: {token_resp.content}")
        return redirect(reverse('auth_failure'))
    token_resp_body = token_resp.json()
    auth_headers = {"Authorization": f"{token_resp_body.get('token_type')} {token_resp_body.get('access_token')}"}

    # Get the user's username, Discord ID and avatar image hash
    name_resp = requests.get('https://discord.com/api/v8/users/@me', headers=auth_headers)
    if name_resp.status_code != 200:
        logger.info(f"Login failed ({name_resp.status_code}) retrieving name: {name_resp.content}")
        return redirect(reverse('auth_failure'))
    name_resp_body = name_resp.json()

    # Check the use is in Tango's Patreon discord channel.
    # Checking any finer detail, for example their role, requires a bot in that channel.
    guilds_resp = requests.get('https://discord.com/api/v8/users/@me/guilds', headers=auth_headers)
    if guilds_resp.status_code != 200:
        logger.info(f"Login failed ({guilds_resp.status_code}) retrieving guilds: {guilds_resp.content}")
        return redirect(reverse('auth_failure'))
    guilds_resp_body = guilds_resp.json()
    if "Tango's Patreon Server" not in [guild['name'] for guild in guilds_resp_body]:
        logger.info(f"Login failed checking guilds")
        return redirect(reverse('auth_failure'))

    # Store all details from Discord and log the user in. Return to index page when completed
    user, _ = User.objects.get_or_create(username=name_resp_body.get('username'))
    user_details, _ = UserDetails.objects.get_or_create(user=user,
                                                        discord_id=name_resp_body.get('id'),
                                                        avatar_hash=name_resp_body.get('avatar'))
    auth.login(request, user)
    return redirect(reverse('index'))


@login_required()
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def auth_failure(request):
    template_name = 'auth_failure.html'
    return render(request, template_name)
