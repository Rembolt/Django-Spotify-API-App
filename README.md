# Django-Spotify-API-App
# 🎵 Power Shuffle Music Player 🎵
A fully customizable music player built to extend Spotify’s shuffle feature, adding new algorithmic and user-driven options for a tailored listening experience. With Power Shuffle Music Player, users can personalize their music queue to match their mood, genres, and preferences—all integrated with the Spotify API. 
![Screenshot 2024-10-25 183707](https://github.com/user-attachments/assets/ad787dd4-f5f3-4ffd-b05a-907ce6f69ae5)
![Screenshot 2025-04-09 140607](https://github.com/user-attachments/assets/af9083f8-90c3-45b4-bddc-c4beecf99432)

## How to Run the Application
1. Go to website: https://powershuffle.ianblanc.com/
2. Log in to your Spotify account and give the app permission to see private Spotify data.
3. Copy the link from a playlist you want to shuffle and paste it into the website link box.
4. Shuffle the playlist into a desired shuffle style.
5. Open Spotify on your device (premium required) and start the Spotify player.
6. Go back to the powershuffle app and click the play button on a shuffled style, and the songs should load on your Spotify queue.
7. Enjoy!

![Screenshot 2024-10-25 184540](https://github.com/user-attachments/assets/bd2253ea-77e4-48ce-8a5f-87d6c616cff6)

## Key Features
Diverse Shuffle Options:
![Screenshot 2024-10-25 184120](https://github.com/user-attachments/assets/579cfef8-d581-46b2-b9c9-786ba0b0caac)
### Knuths
Modern Fiisher Yates Shuffle: This algorithm, described by Donald Knuth in his book "The Art of Computer Programming," generates random permutations by swapping elements in a clever way to achieve uniform distribution.

### Genres
The Genre-Aware Shuffle uses the Fisher-Yates Shuffle and incorporates genre-based sorting using Spotify's genre data. Based on the given probability, the shuffled playlist is adjusted: with 100% probability, songs of the same genre are clustered together, while with 0% probability, songs of the same genre are dispersed. Note that Spotify's genre data may be incomplete, which could affect the sorting accuracy.

### Recent
The Recently Listened Shuffle builds on the Fisher-Yates Shuffle and sorts songs based on your last 150 listened songs. Depending on a given probability, the shuffled playlist is adjusted: with 100% probability, recently listened songs are placed at the beginning of the playlist; with 50% probability, they are interspersed with songs you haven't listened to recently; with 0% probability, they are placed at the end of the queue.

### Authorization flow 
with access tokens to fetch user playlists and track metadata. Display custom queues with song previews, album art, and metadata. Automatically deploy custom queues to Spotify. User Interface: Preview various shuffle types and configurations before selecting the final queue. Color palette options include purple, green, black, and white. 
![Screenshot 2024-10-25 183714](https://github.com/user-attachments/assets/b95be099-e851-4e7f-bebe-09a1c29d7ed8)
![Screenshot 2024-10-25 183728](https://github.com/user-attachments/assets/3ff20577-c3b4-4b6d-b582-cb15c1be1181)

### Tooltips
The app is full of insights on how to use its tools.
![Screenshot 2024-10-25 183835](https://github.com/user-attachments/assets/bf61ec14-6ff2-446e-aa14-5e5cc1f5e5db)
![Screenshot 2024-10-25 184234](https://github.com/user-attachments/assets/bc0c0ec5-90e2-4000-a0e3-906400017ed7)

### Other
Supports for multiple browsers and device dimensions. 
Saves only minimal user data so the app can work.

# Open Source
This app is entirely open source on GitHub, and private Spotify keys and user data are properly secured on the deployment version. (https://github.com/Rembolt/Django-Spotify-API-App/)

## Server Configuration
If you are curious to know how the server is configured, let me give you some info:

The Server is hosted on an AWS EC2 instance and has a DNS link to the actual domain. The project is wrapped on Docker for volume handling and management of:
 	-Certbot, taking care of the HTTPS certification process.
-A reverse proxy using NGINX that manages:
-ssl certification ( and HTTPS HTTP control)
-communicates UWSGI workers
 -Django app running with:
 -WSGI
-Whitenoise to handle Static files (and Media)
-Support for Postgres DataBase
 -PostGress as designated Database
	
Django communicates with the Spotify API through its views and saves only minimal user data so the app can work.


## Additional Information
If any issues arise during execution as instructed, please provide feedback detailing the errors encountered to the following email: ianblancmendes@gmail.com. 
Your assistance is much appreciated.


## Potential Future Features
### Musicality shuffle
Utilizes clustering and distance algorithms (like Fisher-Yates and K-means) to provide genre grouping, mood clusters, artist proximity, and even “musicality” grouping, all to create a highly personalized queue experience.

### Proficient Error Handling
Even though the app has error handling to help the user and developer understand what went wrong, currently, the app does not cover all possible error results.

