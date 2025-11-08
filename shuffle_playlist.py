import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def shuffle_playlist():
    """Shuffle a Spotify playlist by reordering all tracks randomly"""
    
    # Get credentials from environment variables (GitHub Secrets)
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')
    
    # Your playlist ID - REPLACE WITH YOUR ACTUAL PLAYLIST ID
    PLAYLIST_ID = '5oAcZQuWg3EZLav9bf4r4l'
    
    print("=" * 60)
    print("🎵 Spotify Playlist Shuffler")
    print("=" * 60)
    
    # Create Spotify client with refresh token
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://127.0.0.1:8888',
        scope='playlist-modify-public playlist-modify-private'
    )
    
    # Manually set the refresh token
    token_info = auth_manager.refresh_access_token(refresh_token)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    print(f"\n📋 Fetching playlist: {PLAYLIST_ID}")
    
    # Get all tracks from the playlist
    tracks = []
    results = sp.playlist_tracks(PLAYLIST_ID)
    tracks.extend(results['items'])
    
    # Handle pagination for playlists with more than 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    print(f"✓ Found {len(tracks)} tracks in playlist")
    
    # Extract track URIs and shuffle them
    track_uris = [item['track']['uri'] for item in tracks if item['track']]
    
    print(f"\n🔀 Shuffling {len(track_uris)} tracks...")
    random.shuffle(track_uris)
    
    # Replace playlist items with shuffled order
    # Spotify API limits to 100 tracks per request
    print(f"📤 Updating playlist order...")
    sp.playlist_replace_items(PLAYLIST_ID, track_uris[:100])
    
    # Add remaining tracks in batches of 100
    if len(track_uris) > 100:
        for i in range(100, len(track_uris), 100):
            batch = track_uris[i:i+100]
            sp.playlist_add_items(PLAYLIST_ID, batch)
            print(f"   Added batch {i//100 + 1}")
    
    print(f"\n✅ Playlist successfully shuffled!")
    print(f"🎉 {len(track_uris)} tracks have been reordered")
    print("=" * 60)

if __name__ == "__main__":
    try:
        shuffle_playlist()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check:")
        print("  - Your playlist ID is correct")
        print("  - Your secrets are properly set in GitHub")
        print("  - The playlist is owned by you or you have edit permissions")
        raise
