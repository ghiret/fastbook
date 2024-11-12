import requests
from typing import List, Dict, Union
from fastai.vision.utils import download_images
class WikimediaURLFetcher:
    def __init__(self, bot_name="WikiImageBot", version="1.0", 
                 contact_info="your-github-repo-or-email"):
        self.base_url = "https://commons.wikimedia.org/w/api.php"
        # Format: <client name>/<version> (<contact information>) <library name>/<version>
        self.headers = {
            'User-Agent': f'{bot_name}/{version} ({contact_info}) python-requests/{requests.__version__}'
        }
    
    def get_image_urls(self, query: str, limit: int = 100) -> List[Dict[str, str]]:
        """
        Get a list of image URLs from Wikimedia Commons.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of images to fetch (default: 100)
            
        Returns:
            List[Dict[str, str]]: List of dictionaries containing image metadata
                Each dict contains:
                - 'title': Image title
                - 'full_url': URL to full resolution image
                - 'thumb_url': URL to thumbnail (800px width)
        """
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrnamespace": "6",  # File namespace
            "gsrsearch": f"filetype:bitmap {query}",
            "gsrlimit": limit,
            "prop": "imageinfo",
            "iiprop": "url|dimensions|mime",
            "iiurlwidth": 800
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if "query" not in data or "pages" not in data["query"]:
                print("No images found")
                return []
                
            images = []
            for page in data["query"]["pages"].values():
                if "imageinfo" in page:
                    image_info = page["imageinfo"][0]
                    if image_info["mime"].startswith("image/"):
                        images.append({
                            "title": page.get("title", "").replace("File:", ""),
                            "full_url": image_info.get("url", ""),
                            "thumb_url": image_info.get("thumburl", "")
                        })
            
            return images
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images: {e}")
            return []

def download_images_from_fetcher_results(dest: str, bear_type: str = "", limit: int = 100):
    """
    Download bear images to specified destination using fastdownload.
    
    Args:
        dest (str): Destination directory
        bear_type (str): Type of bear (e.g., "polar", "grizzly")
        limit (int): Maximum number of images to download
    """
    fetcher = WikimediaURLFetcher(
        bot_name="BearImageBot",
        version="1.0",
        contact_info="https://github.com/yourusername/bearbot; your.email@example.com"
    )
    query = f"{bear_type} bear" if bear_type else "bear"
    results = fetcher.get_image_urls(query, limit)
    download_images(dest, urls=results.thumb_url)

# Example usage
if __name__ == "__main__":
    # Get the image URLs
    images = get_bear_images(limit=10)
    
    # Print them nicely
    for i, img in enumerate(images, 1):
        print(f"\nImage {i}:")
        print(f"Title: {img['title']}")
        print(f"Thumbnail URL: {img['thumb_url']}")
        print(f"Full resolution URL: {img['full_url']}")