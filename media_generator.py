import requests
import json
import os
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum

class MediaType(Enum):
    """Supported media types for generation"""
    IMAGE = "image"
    VIDEO = "video"
    MUSIC = "music"


class MediaGenerator:
    """
    A comprehensive media generator supporting image, video, and music generation
    using multiple APIs and AI services.
    """
    
    # API Endpoints and Keys
    UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "demo_key")
    PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "demo_key")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "demo_key")
    
    def __init__(self):
        self.session = requests.Session()
        self.media_history = []
        self.generation_count = 0
    
    # ==================== IMAGE GENERATION ====================
    
    def generate_image_unsplash(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate images using Unsplash API.
        
        Args:
            query: Search query for images
            count: Number of images to fetch (1-20)
            
        Returns:
            List of image data dictionaries
        """
        try:
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": min(count, 20),
                "client_id": self.UNSPLASH_API_KEY
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get("results", []):
                image_data = {
                    "source": "Unsplash",
                    "query": query,
                    "url": photo.get("urls", {}).get("regular"),
                    "thumb_url": photo.get("urls", {}).get("thumb"),
                    "title": photo.get("description", photo.get("alt_description", "Untitled")),
                    "photographer": photo.get("user", {}).get("name"),
                    "created_at": datetime.now().isoformat()
                }
                images.append(image_data)
                self.media_history.append(image_data)
            
            return images
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images from Unsplash: {e}")
            return []
    
    def generate_image_pixabay(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate images using Pixabay API.
        
        Args:
            query: Search query for images
            count: Number of images to fetch
            
        Returns:
            List of image data dictionaries
        """
        try:
            url = "https://pixabay.com/api/"
            params = {
                "key": self.PIXABAY_API_KEY,
                "q": query,
                "per_page": min(count, 50),
                "image_type": "photo"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for hit in data.get("hits", []):
                image_data = {
                    "source": "Pixabay",
                    "query": query,
                    "url": hit.get("largeImageURL"),
                    "thumb_url": hit.get("previewURL"),
                    "title": f"Image by {hit.get('user')}",
                    "photographer": hit.get("user"),
                    "created_at": datetime.now().isoformat()
                }
                images.append(image_data)
                self.media_history.append(image_data)
            
            return images
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images from Pixabay: {e}")
            return []
    
    def generate_image(self, query: str, source: str = "unsplash", count: int = 1) -> List[Dict]:
        """
        Generate images from specified source.
        
        Args:
            query: Image search query
            source: Image source (unsplash, pixabay)
            count: Number of images
            
        Returns:
            List of image data
        """
        if source.lower() == "unsplash":
            return self.generate_image_unsplash(query, count)
        elif source.lower() == "pixabay":
            return self.generate_image_pixabay(query, count)
        else:
            print(f"Unknown image source: {source}")
            return []
    
    # ==================== VIDEO GENERATION ====================
    
    def generate_video_pexels(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate videos using Pexels API.
        
        Args:
            query: Search query for videos
            count: Number of videos to fetch
            
        Returns:
            List of video data dictionaries
        """
        try:
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": self.PEXELS_API_KEY}
            params = {
                "query": query,
                "per_page": min(count, 80)
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for video in data.get("videos", []):
                video_data = {
                    "source": "Pexels",
                    "type": "video",
                    "query": query,
                    "title": video.get("url", "Untitled Video"),
                    "url": video.get("url"),
                    "duration": video.get("duration"),
                    "width": video.get("width"),
                    "height": video.get("height"),
                    "photographer": video.get("user", {}).get("name"),
                    "video_files": video.get("video_files", []),
                    "created_at": datetime.now().isoformat()
                }
                videos.append(video_data)
                self.media_history.append(video_data)
            
            return videos
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching videos from Pexels: {e}")
            return []
    
    def generate_video_pixabay(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate videos using Pixabay API.
        
        Args:
            query: Search query for videos
            count: Number of videos to fetch
            
        Returns:
            List of video data dictionaries
        """
        try:
            url = "https://pixabay.com/api/videos/"
            params = {
                "key": self.PIXABAY_API_KEY,
                "q": query,
                "per_page": min(count, 50)
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for hit in data.get("hits", []):
                video_data = {
                    "source": "Pixabay",
                    "type": "video",
                    "query": query,
                    "title": f"Video by {hit.get('user')}",
                    "url": f"https://pixabay.com/videos/download/{hit.get('id')}/",
                    "duration": hit.get("duration"),
                    "photographer": hit.get("user"),
                    "videos": hit.get("videos", {}),
                    "created_at": datetime.now().isoformat()
                }
                videos.append(video_data)
                self.media_history.append(video_data)
            
            return videos
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching videos from Pixabay: {e}")
            return []
    
    def generate_video(self, query: str, source: str = "pexels", count: int = 1) -> List[Dict]:
        """
        Generate videos from specified source.
        
        Args:
            query: Video search query
            source: Video source (pexels, pixabay)
            count: Number of videos
            
        Returns:
            List of video data
        """
        if source.lower() == "pexels":
            return self.generate_video_pexels(query, count)
        elif source.lower() == "pixabay":
            return self.generate_video_pixabay(query, count)
        else:
            print(f"Unknown video source: {source}")
            return []
    
    # ==================== MUSIC GENERATION ====================
    
    def generate_music_freesound(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate music using Freesound API.
        
        Args:
            query: Search query for music
            count: Number of tracks to fetch
            
        Returns:
            List of music data dictionaries
        """
        try:
            # Note: Freesound requires API key from https://freesound.org/api/apply/
            api_key = os.getenv("FREESOUND_API_KEY", "demo_key")
            url = "https://freesound.org/api/v2/search/text/"
            params = {
                "query": query,
                "page_size": min(count, 50),
                "token": api_key,
                "filter": "tags:(music OR instrumental)"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tracks = []
            
            for sound in data.get("results", []):
                track_data = {
                    "source": "Freesound",
                    "type": "music",
                    "query": query,
                    "title": sound.get("name"),
                    "url": sound.get("previews", {}).get("preview-hq-mp3"),
                    "duration": sound.get("duration"),
                    "license": sound.get("license"),
                    "artist": sound.get("username"),
                    "tags": sound.get("tags", []),
                    "created_at": datetime.now().isoformat()
                }
                tracks.append(track_data)
                self.media_history.append(track_data)
            
            return tracks
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching music from Freesound: {e}")
            return []
    
    def generate_music_zenodo(self, query: str, count: int = 1) -> List[Dict]:
        """
        Generate music using Zenodo API (open access).
        
        Args:
            query: Search query for music
            count: Number of tracks to fetch
            
        Returns:
            List of music data dictionaries
        """
        try:
            url = "https://zenodo.org/api/records"
            params = {
                "q": f"{query} AND (filetype:mp3 OR filetype:wav OR keywords:music)",
                "size": min(count, 50),
                "sort": "bestmatch"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tracks = []
            
            for record in data.get("hits", {}).get("hits", []):
                files = record.get("files", [])
                audio_files = [f for f in files if f.get("type") in ["mp3", "wav", "flac"]]
                
                if audio_files:
                    track_data = {
                        "source": "Zenodo",
                        "type": "music",
                        "query": query,
                        "title": record.get("metadata", {}).get("title"),
                        "url": record.get("links", {}).get("self_html"),
                        "creators": record.get("metadata", {}).get("creators", []),
                        "files": audio_files,
                        "created_at": datetime.now().isoformat()
                    }
                    tracks.append(track_data)
                    self.media_history.append(track_data)
            
            return tracks
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching music from Zenodo: {e}")
            return []
    
    def generate_music(self, query: str, source: str = "freesound", count: int = 1) -> List[Dict]:
        """
        Generate music from specified source.
        
        Args:
            query: Music search query
            source: Music source (freesound, zenodo)
            count: Number of tracks
            
        Returns:
            List of music data
        """
        if source.lower() == "freesound":
            return self.generate_music_freesound(query, count)
        elif source.lower() == "zenodo":
            return self.generate_music_zenodo(query, count)
        else:
            print(f"Unknown music source: {source}")
            return []
    
    # ==================== UTILITY METHODS ====================
    
    def format_media(self, media_data: Dict) -> str:
        """Format media data for display."""
        if not media_data:
            return "No media to display."
        
        output = []
        media_type = media_data.get("type", media_data.get("source"))
        
        output.append(f"📁 Type: {media_type.upper()}")
        output.append(f"📚 Source: {media_data.get('source', 'Unknown')}")
        output.append(f"🏷️  Title: {media_data.get('title', 'Untitled')}")
        
        if media_data.get("photographer"):
            output.append(f"👤 Creator: {media_data.get('photographer')}")
        elif media_data.get("artist"):
            output.append(f"👤 Artist: {media_data.get('artist')}")
        elif media_data.get("creators"):
            creators = [c.get("name", "Unknown") for c in media_data.get("creators", [])]
            output.append(f"👤 Creators: {', '.join(creators)}")
        
        if media_data.get("url"):
            output.append(f"🔗 URL: {media_data.get('url')}")
        
        if media_data.get("duration"):
            output.append(f"⏱️  Duration: {media_data.get('duration')}s")
        
        if media_data.get("width") and media_data.get("height"):
            output.append(f"📐 Resolution: {media_data.get('width')}x{media_data.get('height')}")
        
        if media_data.get("tags"):
            output.append(f"🏷️  Tags: {', '.join(media_data.get('tags')[:5])}")
        
        return "\n".join(output)
    
    def get_media_history(self) -> List[Dict]:
        """Get all generated media."""
        return self.media_history
    
    def clear_history(self):
        """Clear the media history."""
        self.media_history = []
    
    def save_history(self, filename: str):
        """Save media history to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.media_history, f, indent=2)
        print(f"✅ Media history saved to {filename}")
    
    def get_stats(self) -> Dict:
        """Get generation statistics."""
        media_types = {}
        sources = {}
        
        for media in self.media_history:
            media_type = media.get("type", "unknown")
            source = media.get("source", "unknown")
            
            media_types[media_type] = media_types.get(media_type, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_generated": len(self.media_history),
            "by_type": media_types,
            "by_source": sources
        }


def main():
    """Main function to run the interactive media generator."""
    print("=" * 70)
    print("🎨 Welcome to the AI Media Generator! 🎵 🎬")
    print("=" * 70)
    print("\n📸 IMAGE Commands:")
    print("  /img <query>        - Generate images (Unsplash)")
    print("  /img <query> <src>  - Generate images (unsplash/pixabay)")
    print("  /img <query> <n>    - Generate n images")
    print("\n🎬 VIDEO Commands:")
    print("  /vid <query>        - Generate videos (Pexels)")
    print("  /vid <query> <src>  - Generate videos (pexels/pixabay)")
    print("  /vid <query> <n>    - Generate n videos")
    print("\n🎵 MUSIC Commands:")
    print("  /music <query>      - Generate music (Freesound)")
    print("  /music <query> <s>  - Generate music (freesound/zenodo)")
    print("  /music <query> <n>  - Generate n tracks")
    print("\n📋 UTILITY Commands:")
    print("  /history            - Show all generated media")
    print("  /stats              - Show generation statistics")
    print("  /save               - Save history to file")
    print("  /clear              - Clear history")
    print("  /exit               - Exit the program")
    print("\n" + "=" * 70 + "\n")
    
    generator = MediaGenerator()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == "/exit":
                print("\n👋 Thanks for creating! Goodbye!")
                break
            
            elif command == "/img" or command == "/image":
                if len(parts) < 2:
                    print("❌ Usage: /img <query> [source] [count]\n")
                    continue
                
                query = parts[1]
                source = parts[2] if len(parts) > 2 else "unsplash"
                count = int(parts[3]) if len(parts) > 3 else 1
                
                print(f"\n🔍 Searching for images: '{query}'...\n")
                images = generator.generate_image(query, source, count)
                
                if images:
                    for i, img in enumerate(images, 1):
                        print(f"--- Image {i} ---")
                        print(generator.format_media(img) + "\n")
                else:
                    print("❌ No images found.\n")
            
            elif command == "/vid" or command == "/video":
                if len(parts) < 2:
                    print("❌ Usage: /vid <query> [source] [count]\n")
                    continue
                
                query = parts[1]
                source = parts[2] if len(parts) > 2 else "pexels"
                count = int(parts[3]) if len(parts) > 3 else 1
                
                print(f"\n🔍 Searching for videos: '{query}'...\n")
                videos = generator.generate_video(query, source, count)
                
                if videos:
                    for i, vid in enumerate(videos, 1):
                        print(f"--- Video {i} ---")
                        print(generator.format_media(vid) + "\n")
                else:
                    print("❌ No videos found.\n")
            
            elif command == "/music":
                if len(parts) < 2:
                    print("❌ Usage: /music <query> [source] [count]\n")
                    continue
                
                query = parts[1]
                source = parts[2] if len(parts) > 2 else "freesound"
                count = int(parts[3]) if len(parts) > 3 else 1
                
                print(f"\n🔍 Searching for music: '{query}'...\n")
                tracks = generator.generate_music(query, source, count)
                
                if tracks:
                    for i, track in enumerate(tracks, 1):
                        print(f"--- Track {i} ---")
                        print(generator.format_media(track) + "\n")
                else:
                    print("❌ No music found.\n")
            
            elif command == "/history":
                if not generator.media_history:
                    print("\n📭 No media in history yet.\n")
                else:
                    print(f"\n📊 Showing {len(generator.media_history)} media items:\n")
                    for i, media in enumerate(generator.media_history, 1):
                        print(f"--- Media {i} ---")
                        print(generator.format_media(media) + "\n")
            
            elif command == "/stats":
                stats = generator.get_stats()
                print(f"\n📊 Statistics:")
                print(f"Total generated: {stats['total_generated']}")
                print(f"By type: {stats['by_type']}")
                print(f"By source: {stats['by_source']}\n")
            
            elif command == "/save":
                filename = f"media_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                generator.save_history(filename)
                print()
            
            elif command == "/clear":
                generator.clear_history()
                print("🗑️  History cleared.\n")
            
            else:
                print("❌ Unknown command. Type /exit to quit.\n")
        
        except ValueError as e:
            print(f"❌ Invalid input: {e}\n")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
