"""
Main web scraping application for finding course creator leads.
"""
import os
import json
import csv
from datetime import datetime
from typing import List
from dotenv import load_dotenv

from base_scraper import Lead
from hotmart_scraper import HotmartScraper
from instagram_scraper import InstagramScraper
from google_scraper import GoogleScraper


class LeadScraper:
    """Main class to orchestrate all platform scrapers."""
    
    def __init__(self, max_results_per_platform: int = 50):
        load_dotenv()
        self.max_results = max_results_per_platform
        self.all_leads: List[Lead] = []
        
        # Initialize scrapers
        self.hotmart_scraper = HotmartScraper(self.max_results)
        self.instagram_scraper = InstagramScraper(self.max_results)
        self.google_scraper = GoogleScraper(self.max_results)
    
    def scrape_all_platforms(self, filter_mec: bool = True, 
                            min_engagement: float = 0.5) -> List[Lead]:
        """Scrape all platforms and aggregate results."""
        print("🔍 Starting web scraping for course creator leads...\n")
        
        # Scrape Hotmart
        print("📚 Scraping Hotmart...")
        hotmart_leads = self.hotmart_scraper.get_leads(filter_mec, min_engagement)
        print(f"   Found {len(hotmart_leads)} leads on Hotmart\n")
        
        # Scrape Instagram
        print("📱 Scraping Instagram...")
        instagram_leads = self.instagram_scraper.get_leads(filter_mec, min_engagement)
        print(f"   Found {len(instagram_leads)} leads on Instagram\n")
        
        # Scrape Google
        print("🌐 Scraping Google Search...")
        google_leads = self.google_scraper.get_leads(filter_mec, min_engagement)
        print(f"   Found {len(google_leads)} leads on Google\n")
        
        # Aggregate all leads
        self.all_leads = hotmart_leads + instagram_leads + google_leads
        
        print(f"✅ Total leads found: {len(self.all_leads)}")
        print(f"   - Hotmart: {len(hotmart_leads)}")
        print(f"   - Instagram: {len(instagram_leads)}")
        print(f"   - Google: {len(google_leads)}\n")
        
        return self.all_leads
    
    def export_to_csv(self, filename: str = None):
        """Export leads to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"leads_{timestamp}.csv"
        
        if not self.all_leads:
            print("⚠️  No leads to export. Run scrape_all_platforms() first.")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'platform', 'url', 'engagement_score', 
                         'followers', 'description', 'mentions_mec']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for lead in self.all_leads:
                writer.writerow(lead.to_dict())
        
        print(f"💾 Leads exported to: {filepath}")
        return filepath
    
    def export_to_json(self, filename: str = None):
        """Export leads to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"leads_{timestamp}.json"
        
        if not self.all_leads:
            print("⚠️  No leads to export. Run scrape_all_platforms() first.")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        # Convert leads to dict (generator-friendly approach for large datasets)
        leads_data = (lead.to_dict() for lead in self.all_leads)
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            # Write JSON manually for better memory efficiency with large datasets
            jsonfile.write('[\n')
            for i, lead_dict in enumerate(leads_data):
                if i > 0:
                    jsonfile.write(',\n')
                json.dump(lead_dict, jsonfile, indent=2, ensure_ascii=False)
            jsonfile.write('\n]')
        
        print(f"💾 Leads exported to: {filepath}")
        return filepath
    
    def print_summary(self):
        """Print a summary of the leads found."""
        if not self.all_leads:
            print("No leads found.")
            return
        
        print("\n" + "="*60)
        print("LEAD SUMMARY")
        print("="*60 + "\n")
        
        # Group by platform
        by_platform = {}
        for lead in self.all_leads:
            if lead.platform not in by_platform:
                by_platform[lead.platform] = []
            by_platform[lead.platform].append(lead)
        
        for platform, leads in by_platform.items():
            print(f"\n{platform} ({len(leads)} leads):")
            print("-" * 60)
            
            # Sort by engagement score
            sorted_leads = sorted(leads, key=lambda x: x.engagement_score, reverse=True)
            
            for i, lead in enumerate(sorted_leads[:5], 1):  # Show top 5
                print(f"{i}. {lead.name}")
                print(f"   URL: {lead.url}")
                print(f"   Engagement: {lead.engagement_score:.2f}")
                print(f"   Followers: {lead.followers}")
                print(f"   Description: {lead.description[:80]}...")
                print()


def main():
    """Main function to run the scraper."""
    print("=" * 60)
    print("LEAD SCRAPER - Course Creators Finder")
    print("=" * 60 + "\n")
    
    # Configuration
    try:
        max_results = int(os.getenv('MAX_RESULTS_PER_PLATFORM', 50))
    except ValueError:
        print("⚠️  Invalid MAX_RESULTS_PER_PLATFORM value. Using default: 50")
        max_results = 50
    
    output_format = os.getenv('OUTPUT_FORMAT', 'csv').lower()
    
    # Initialize scraper
    scraper = LeadScraper(max_results_per_platform=max_results)
    
    # Scrape all platforms
    # filter_mec=True excludes leads that mention MEC
    # min_engagement=0.5 only includes leads with decent engagement
    leads = scraper.scrape_all_platforms(filter_mec=True, min_engagement=0.5)
    
    # Print summary
    scraper.print_summary()
    
    # Export results
    if output_format == 'json':
        scraper.export_to_json()
    else:
        scraper.export_to_csv()
    
    print("\n✨ Scraping completed successfully!")


if __name__ == "__main__":
    main()
