import logging
import urllib

import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from app import utils
from app.models.constants import Region
from app.models.locations import Location, Maintainer
from app.models.users import UserDetails

logger = logging.getLogger()


def is_maintainer(user, slug):
    location = Location.objects.get(slug=slug)
    maintainers = Maintainer.objects.filter(location=location)
    return user in [m.user for m in maintainers]


def index(request):
    template_name = 'pages/index.html'
    context = {}
    return render(request, template_name, context)


def auth_failure(request):
    template_name = 'pages/auth_failure.html'
    return render(request, template_name)


def not_authorised(request):
    """For when a logged in user attempts to access another user's resources"""
    template_name = 'pages/unauthorised.html'
    return render(request, template_name)


def login(request):
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
        'redirect_uri': host + reverse('verify_callback'),
        'response_type': 'code',
        'scope': 'identify guilds',
        'prompt': 'none'  # Skips auth screen if they've already authorised
    }
    url = base_url + urllib.parse.urlencode(params)
    return redirect(url)


def verify_callback(request):
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
        'redirect_uri': host + reverse('verify_callback'),
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


@login_required()
def list_stock(request):
    template_name = 'pages/list_stock.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def list_services(request):
    template_name = 'pages/list_services.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def list_farms(request):
    template_name = 'pages/list_farms.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def list_locations(request, region):
    template_name = 'pages/list_locations.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def manage_locations(request):
    template_name = 'pages/manage_locations.html'
    locations = [m.location for m in Maintainer.objects.filter(user=request.user)]
    context = {
        "locations": locations
    }
    return render(request, template_name, context)


@login_required()
def get_location(request, slug):
    template_name = 'pages/get_location.html'

    location = Location.objects.get(slug=slug)
    maintainers = Maintainer.objects.filter(location=location)

    maintainer_details = []
    for maintainer in maintainers:
        details = UserDetails.objects.get(user=maintainer.user)
        maintainer_details.append({
            "username": maintainer.user.username,
            "avatar": f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"
        })

    context = {
        "is_maintainer": request.user in [m.user for m in maintainers],
        "location": location,
        "maintainers": maintainer_details
    }
    return render(request, template_name, context)


@login_required()
def modify_location(request, slug):
    template_name = 'pages/modify_location.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    location = Location.objects.get(slug=slug)
    context = {
        "location": location
    }
    return render(request, template_name, context)


@login_required()
def modify_maintainers(request, slug):
    template_name = 'pages/modify_maintainers.html'
    location = Location.objects.get(slug=slug)
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    maintainers = Maintainer.objects.filter(location=location)
    for maintainer in maintainers:
        details = UserDetails.objects.get(user=maintainer.user)
        maintainer.avatar = f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"

    context = {
        "location": location,
        "maintainers": maintainers,
        "users": User.objects.all()
    }
    return render(request, template_name, context)


@login_required()
def modify_stock(request, slug):
    template_name = 'pages/modify_stock.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def modify_services(request, slug):
    template_name = 'pages/modify_services.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def modify_farmables(request, slug):
    template_name = 'pages/modify_farmables.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def add_location(request):
    location, _ = Location.objects.get_or_create(name=request.POST['name'])
    if request.POST.get("delete"):
        location.delete()
        return redirect(reverse("manage_locations"))

    location.description = request.POST['description']
    location.x_pos = int(request.POST['x_pos'])
    location.y_pos = int(request.POST['y_pos'])
    location.z_pos = int(request.POST['z_pos'])
    location.region = Region.objects.get(name=request.POST['region'])

    location.save()
    maintainer, _ = Maintainer.objects.get_or_create(
        location=location,
        user=request.user
    )
    maintainer.save()
    return redirect(reverse("get_location", args=(location.slug,)))


@login_required()
def add_maintainer(request):
    location = Location.objects.get(id=request.POST['location'])
    maintainer = Maintainer(
        location=location,
        user=User.objects.get(id=request.POST['user'])
    )
    maintainer.save()
    return redirect(reverse("modify_maintainers", args=(location.slug,)))


@login_required()
def delete_maintainer(request):
    maintainer = Maintainer.objects.get(id=request.POST['id'])
    location_slug = maintainer.location.slug
    maintainer.delete()
    return redirect(reverse("modify_maintainers", args=(location_slug,)))
