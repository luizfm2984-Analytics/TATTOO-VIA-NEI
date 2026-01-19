"""
Base scraper module with common functionality for all platform scrapers.
"""
from typing import List, Dict
from abc import ABC, abstractmethod


class Lead:
    """Represents a course creator lead."""
    
    def __init__(self, name: str, platform: str, url: str, 
                 engagement_score: float = 0.0, 
                 followers: int = 0,
                 description: str = ""):
        self.name = name
        self.platform = platform
        self.url = url
        self.engagement_score = engagement_score
        self.followers = followers
        self.description = description
        self.mentions_mec = False
        
    def check_mec_mentions(self):
        """Check if the lead mentions MEC in their description."""
        mec_keywords = [
            'mec', 'ministério da educação', 'ministerio da educacao',
            'autorizado mec', 'reconhecido mec', 'credenciado mec',
            'mec reconhecido', 'diploma mec'
        ]
        text = self.description.lower()
        self.mentions_mec = any(keyword in text for keyword in mec_keywords)
        return self.mentions_mec
    
    def to_dict(self) -> Dict:
        """Convert lead to dictionary format."""
        return {
            'name': self.name,
            'platform': self.platform,
            'url': self.url,
            'engagement_score': self.engagement_score,
            'followers': self.followers,
            'description': self.description,
            'mentions_mec': self.mentions_mec
        }


class BaseScraper(ABC):
    """Base class for all platform scrapers."""
    
    def __init__(self, max_results: int = 50):
        self.max_results = max_results
        self.leads: List[Lead] = []
    
    @abstractmethod
    def scrape(self) -> List[Lead]:
        """Scrape leads from the platform."""
        pass
    
    def filter_by_mec(self, leads: List[Lead]) -> List[Lead]:
        """Filter out leads that mention MEC."""
        filtered = []
        for lead in leads:
            lead.check_mec_mentions()
            if not lead.mentions_mec:
                filtered.append(lead)
        return filtered
    
    def filter_by_engagement(self, leads: List[Lead], 
                            min_score: float = 0.5) -> List[Lead]:
        """Filter leads by minimum engagement score."""
        return [lead for lead in leads if lead.engagement_score >= min_score]
    
    def get_leads(self, filter_mec: bool = True, 
                  min_engagement: float = 0.5) -> List[Lead]:
        """Get all leads with applied filters."""
        leads = self.scrape()
        
        if filter_mec:
            leads = self.filter_by_mec(leads)
        
        if min_engagement > 0:
            leads = self.filter_by_engagement(leads, min_engagement)
        
        return leads
