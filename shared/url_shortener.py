import random
import aiohttp
from typing import Optional, Dict
from shared.config import config

class URLShortener:
    def __init__(self):
        self.shorteners = config.get_url_shorteners()
        self.shortener_list = list(self.shorteners.keys())
    
    def get_random_shortener(self) -> Optional[Dict[str, str]]:
        if not self.shortener_list:
            return None
        
        shortener_name = random.choice(self.shortener_list)
        return self.shorteners[shortener_name]
    
    async def shorten_url(self, destination_url: str) -> Optional[str]:
        shortener = self.get_random_shortener()
        
        if not shortener:
            return None
        
        api_token = shortener['api_token']
        base_url = shortener['base_url']
        
        try:
            url = f"{base_url}?api={api_token}&url={destination_url}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'shortenedUrl' in data:
                            return data['shortenedUrl']
                        elif 'shorturl' in data:
                            return data['shorturl']
                        elif 'short_url' in data:
                            return data['short_url']
                        elif isinstance(data, dict) and 'url' in data:
                            return data['url']
                        
                        return None
            
        except Exception as e:
            print(f"Error shortening URL: {e}")
            return None
    
    def get_whitelist_domains(self) -> list:
        domains = []
        for shortener in self.shorteners.values():
            base_url = shortener['base_url']
            
            if '://' in base_url:
                domain = base_url.split('://')[1].split('/')[0]
            else:
                domain = base_url.split('/')[0]
            
            domains.append(domain)
        
        return domains

url_shortener = URLShortener()
