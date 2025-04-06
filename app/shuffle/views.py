from difflib import SequenceMatcher
import os
import json, random, base64, requests
import re, ast
import urllib.parse as urlparse
from urllib.parse import urlencode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.
from .forms import LinkForm
from .models import User

linkForm = LinkForm()
shuffles =[
    {
        'title':'Knuths',
        'description': 'Modern Fiisher Yates Shuffle: This algorithm, described by Donald Knuth in his book "The Art of Computer Programming," generates random permutations by swapping elements in a clever way to achieve uniform distribution.',
        'songs': ''
    },
    {
        'title':'Genres',
        'description': "The Genre-Aware Shuffle uses the Fisher-Yates Shuffle and incorporates genre-based sorting using Spotify's genre data. Based on the given probability, the shuffled playlist is adjusted: with 100% probability, songs of the same genre are clustered together, while with 0% probability, songs of the same genre are dispersed. Note that Spotify's genre data may be incomplete, which could affect the sorting accuracy.",
        'songs': ''
    },
    {
        'title':'Recent',
        'description': "The Recently Listened Shuffle builds on the Fisher-Yates Shuffle and sorts songs based on your last 150 listened songs. Depending on a given probability, the shuffled playlist is adjusted: with 100% probability, recently listened songs are placed at the beginning of the playlist; with 50% probability, they are interspersed with songs you haven't listened to recently; with 0% probability, they are placed at the end of the queue.",
        'songs': ''
    }
]
# Handle the index page rendering, check if the user is authenticated, and render appropriate content
def index(request, shuffles = shuffles, message = ''):
    print(request.build_absolute_uri(reverse('shuffle:authorize')).replace("http://", "https://"))
    if request.user.is_authenticated:
        if len(shuffles) >= 1:
            return render(request, "shuffle/index.html",{
                'title': 'home',
                'shuffles': shuffles,
                'user': request.user,
                'link_form': linkForm,
                'message': message
            })
        else:
            return render(request, "shuffle/index.html",{
                'title': 'home',
                'shuffles': shuffles,
                'user': request.user,
                'link_form': linkForm,
                'message': message
            })
    else:
        return render(request, "shuffle/index.html",{
            'title': 'home',
            'shuffles': shuffles,
            'user': request.user,
            'link_form': linkForm,
            'message': message
        })

# Handle Spotify authorization by obtaining a code and exchanging it for an access token
def authorize(request):

    client_id = '1489e2a8cc7a435692214a119f7b3655'
    # Obtain the authorization code from the request
    code = request.GET.get('code', '')
    error = request.GET.get('error', '')
    if error== 'access_denied':
        #unathorized. # Redirect the user if authorization is denied
         return index(request, "Access Denied. Try again!")
    elif code:
         # Exchange the authorization code for an access token
        authorization = base64aAuthorizationCode()

        url= 'https://accounts.spotify.com/api/token'
        params= {
            'code': code,
            'redirect_uri': request.build_absolute_uri(reverse('shuffle:authorize')).replace("http://", "https://"),
            'grant_type': 'authorization_code'
        }
        headers={
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': authorization,
        }

        response = apiHandler.post(request,url,params,headers)
        print("signed up")
        print("response: ", response)
        return appHandler.signup(request, response)
    else:
       # Redirect user to Spotify's authorization page if code is not present
        url = "https://accounts.spotify.com/authorize?" 
        params = {  
        'response_type':'code',
        'client_id': client_id,
        'scope': 'user-read-private user-read-email user-library-read user-read-recently-played user-top-read playlist-read-collaborative playlist-read-private user-read-currently-playing user-modify-playback-state user-read-playback-state',
        'redirect_uri': request.build_absolute_uri(reverse('shuffle:authorize')).replace("http://", "https://"),
        'state': ''.join(random.choice('0123456789ABCDEF') for i in range(16)),
        'show_dialog': 'true',
        }
        return apiHandler.httpRedirect(url, params) 
    
def postPlaylist(request, shuffle):
    # Handle POST requests to add songs to the user's Spotify queue based on the selected shuffle
    if request.method == "POST":
        user = request.user
        count = 100
        # print(user.lastPlaylist)
        queue = ast.literal_eval(user.lastPlaylist)
        if queue == None:
            return index(request, shuffles, 'Songs were not retrieved.')
        for i in queue:
            if(i['title'] == shuffle):
                # Iterate through the songs in the queue and add them to the user's Spotify queue
                for song in i['songs']:
                    appHandler.refresh(request)
                    url = "https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A" + song['id'] 
                    header = {'Authorization': 'Bearer ' + request.user.accessToken}
                    response = apiHandler.post(request,url,'',header)
                    if(count<0):
                        break
                    count-=1
                    print(count)
        # Handle the response and update the index page with a success or error message
        if(response == None):
            return index(request, shuffles, 'Songs Were deployed succefully!')
        else:
            return index(request, shuffles, response)
    
def getPlaylist(request):
    # Handle POST requests to retrieve a playlist from Spotify
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            # Validate the submitted form and extract playlist information
            link = form.cleaned_data['link']
            genreCheck = form.cleaned_data['genreCheck']
            if(genreCheck == None):genreCheck=False
            recentCheck = form.cleaned_data['recentCheck']
            if(recentCheck == None):recentCheck=False
            recentPercentage = form.cleaned_data['recentPercentage']
            if(recentPercentage == None):recentPercentage=25
            similarityPercentage = form.cleaned_data['similarityPercentage']
            if(similarityPercentage == None):similarityPercentage=100
        else:
            return index(request, '', 'Info Bellow Invalid!')

        m = re.match(r".*playlist/(\w*)\\?.*", link)
        # Extract the playlist ID from the link
        if m == None:
            message = 'The playlist URL format is invalid.'
            print(message)
            return index(request, '', message)
        else:
            playlistId = m.group(1)
       
        songs = []
        total = 1
        
        while len(songs) < total:
            # Retrieve the songs from the playlist using Spotify API, handling pagination if necessary
            appHandler.refresh(request)
            url = "https://api.spotify.com/v1/playlists/" + playlistId + "/tracks"
            params = {
                'playlist_id': playlistId,
                'fields':'total,items(track(album(images.url),artists(genres, name, id),id,name))',
                'limit': 50,
                'offset': len(songs)
            }
            header = {'Authorization': 'Bearer ' + request.user.accessToken}
            response = apiHandler.get(request,url,params,header)

            if response == None or 'error' in response:
                message = response['error']['message']
                print(message)
                return index(request, '', message)

            total = response['total']
            for track in response['items']:
                songs.append(track['track'])

        # Update the shuffles with the retrieved songs and apply selected shuffling methods
        knuth = knuthShuffle(songs)
        shuffles[0]['songs']= knuth
        if(genreCheck):
            shuffles[1]['songs'] = genreShuffle(request, knuth, similarityPercentage)
        else:
            shuffles[1]['songs'] = ''
        if(recentCheck):
            shuffles[2]['songs']= recentShuffle(request, knuth, recentPercentage)
        else:
            shuffles[2]['songs'] = ''
        
        # Save the last playlist to the user's profile
        request.user.lastPlaylist = str(shuffles)
        request.user.save()
        
        return index(request, shuffles, '')
        
def knuthShuffle(li):
    # Knuth shuffle algorithm to generate a random permutation of the songs
    songs = li[:]
    for i in range(len(songs)-1, 1, -1):
        r = random.SystemRandom().randint(0, i)
        songs[r], songs[i] = songs[i], songs[r]
    return songs

def genreShuffle(request,li, similarity):
    # Genre-aware shuffle algorithm to cluster or disperse songs based on genre similarity
    songs = li[:]
    genres = [[]]
    for song in songs:
        # Retrieve the artist's genre information from Spotify API
        appHandler.refresh(request)
        artistId = song["artists"][0]["id"]
        url = "https://api.spotify.com/v1/artists/" + artistId
        params = {
                'id': artistId
            }
        header = {'Authorization': 'Bearer ' + request.user.accessToken}
        response = apiHandler.get(request,url,params,header)
        if response['genres'] == []:
            genres.append([song, ['N/A']])
        else:
            genres.append([song, response['genres']])
    
    genres.pop(0)
    size = len(genres)
    # Sort the songs based on genre similarity or dissimilarity
    for x in range(size-3):
        r = random.SystemRandom().randint(0, 100)
        closestR = SequenceMatcher(None, str(genres[x][1]), str(genres[x+1][1])).ratio()
        
        closestJ = x+1
        if r < similarity:
            for j in range(x+2,size-1):
                ratio = SequenceMatcher(None, str(genres[x][1]), str(genres[j][1])).ratio()
                if ratio > closestR:
                    closestR= ratio
                    closestJ= j
                if ratio == 1:
                    break
        else:
             for j in range(x+2,size-1):
                ratio = SequenceMatcher(None, str(genres[x][1]), str(genres[j][1])).ratio()
                if ratio < closestR:
                    closestR= ratio
                    closestJ= j
                if ratio < 0.3:
                    break
        genres[x+1], genres[closestJ] = genres[closestJ], genres[x+1]
        songs[x] = genres[x][0]
    
    songs[size-2] = genres[size-2][0]
    songs[size-1] = genres[size-1][0]

    return songs


def recentShuffle(request,li, recent):
    # Recently listened shuffle algorithm to position recently played songs within the playlist
    songs = li[:]
    length=len(songs)
    searches = 10
    i=0
    before = datetime.now()
    before = int(before.timestamp()) * 1000
    for x in range(searches):
        # Retrieve recently played songs from Spotify API
        appHandler.refresh(request)
        url = "https://api.spotify.com/v1/me/player/recently-played"
        params = {
                'limit': 50,
                'before': before
            }
        header = {'Authorization': 'Bearer ' + request.user.accessToken}
        response = apiHandler.get(request,url,params,header)
        try:
           before = response['cursors']['before']
           print(before)
        except TypeError:
            if(length<(x+1)*50):
                return songs
            else:
                print('could not load recent songs error')
                return index(request, '', 'could not load recent songs error')
        for song in response['items']:
            # Sort the songs based on recent listening history and given probability
            for j in range(length):
                if(song['track']['id'] == songs[j]['id']):
                    try:
                        if songs[j]['checked'] == True:
                            break
                    except KeyError:
                        songs[j]['checked'] = True
                        r = random.SystemRandom().randint(0, 100)
                        if r < recent:
                            songs[i], songs[j] = songs[j], songs[i]
                        else:
                            songs[length-i-1], songs[j] = songs[j], songs[length-i-1]
                        i+=1
                        break
    return songs

def base64aAuthorizationCode():
    # Encode client ID and secret for Spotify API authorization
    client_id = '1489e2a8cc7a435692214a119f7b3655'
    leu = "\x39\x35\x32\x37\x62\x36\x31\x66\x36\x36\x39\x30\x34\x35\x66\x64\x61\x64\x63\x66\x38\x38\x30\x64\x64\x39\x65\x63\x30\x33\x35\x61"
    lau = leu.encode("windows-1252").decode("utf-8")
    string = client_id + ':' + lau
    string_bytes = string.encode("ascii") 
    base64_bytes = base64.b64encode(string_bytes) 
    base64_string = base64_bytes.decode("ascii") 
    authorization = 'Basic ' + base64_string

    return authorization
    
class appHandler():
    # Refresh the user's Spotify access token if expired
    def refresh(request):
        if request.user.is_authenticated:
            # appHandler.signOut(request)
            authorization = base64aAuthorizationCode()
            user = request.user
            now = datetime.now()
            then = user.tokenRequestTime.replace(tzinfo=None)
            delta = now - then
            print(delta)
            if(delta.seconds > user.tokenMaxTime):
                appHandler.signOut(request)
                # url= 'https://accounts.spotify.com/api/token'
                # params= {
                #     'grant_type': 'refresh_token',
                #     'refresh_token': user.refreshToken
                    
                # }
                # headers={
                #     'content-type': 'application/x-www-form-urlencoded',
                #     'Authorization': authorization,
                # }

                # response = requests.post(request, url, params=params, headers=headers)
                # response= json.loads(response.text)

                # user.accessToken = response['access_token']
                # user.tokenRequestTime = datetime.now()
                # user.tokenMaxTime = response['expires_in']
                # print('oi')
                
    def signup(request, data):
        # Signup or update the user profile with Spotify account information
        token = data['access_token']
        refreshToken = data['refresh_token']
        tokenMaxTime = data['expires_in']
        url = 'https://api.spotify.com/v1/me'
        header = {'Authorization': 'Bearer ' + token}
        response = apiHandler.get(request,url,'',header)
        print(response)

        #user info:
        email = response['email']
        username = response['display_name']
        profilePic = response['images'][0]['url']
        
        try:
            user = User.objects.get(username=username, email=email)
            if user is not None:
                user.accessToken = token
                user.refreshToken = refreshToken
                user.tokenMaxTime = tokenMaxTime
                user.tokenRequestTime = datetime.now()
                user.profilePic = profilePic
                user.save()
                login(request, user)
                print('user logged in')
                return HttpResponseRedirect(reverse("shuffle:index"))
            else:
                print('user did not log in')
                return index(request, "Something went wrong! Try again later.")
        except User.DoesNotExist:
            try:
                user = User.objects.create_user(username,email)
                user.accessToken = token
                user.refreshToken = refreshToken
                user.tokenMaxTime = tokenMaxTime
                user.tokenRequestTime = datetime.now()
                user.profilePic = profilePic
                user.lastPlaylist= str(shuffles)
                user.save()
                #login(request, user)
                print('user was created')
            except IntegrityError as e:
                print(e)
                print(datetime.now())
                print('user was not created')
                return index(request, "Something went wrong! Try again later.")
            login(request, user)
            print('user logged in')
            return HttpResponseRedirect(reverse('shuffle:index'))
    
    def signOut(request):
        # Log out the user and redirect to the index page
        logout(request)
        return HttpResponseRedirect(reverse('shuffle:index'))
            
                
                
        

        


    # def logout():
 
class apiHandler():

    def httpRedirect(url, params):
        # Redirect to a URL with the given parameters
        url_parts = list(urlparse.urlparse(url))

        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        redirect = HttpResponseRedirect(urlparse.urlunparse(url_parts))

        return redirect
    
    def post(request,url,params,headers):
        # Make a POST request to the given URL and return the response
        response = requests.post(url, params=params, headers=headers)
        if response.status_code != 204:   
            try:
                parsed_response = json.loads(response.text)
                return parsed_response
            except ValueError:
                print(response.text)
                return index(request, str(response.text))
            
    def get(request,url,params,headers):
        # Make a GET request to the given URL and return the response
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 204:
            try:
                parsed_response = json.loads(response.text)
                return parsed_response
            except ValueError:
                print(response.text)
                return index(request, str(response.text))


    # def get():

    


        


