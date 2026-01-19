"""
Example usage of the lead scraper - demonstrates different ways to use the tool.
"""
from main import LeadScraper
from hotmart_scraper import HotmartScraper
from instagram_scraper import InstagramScraper
from google_scraper import GoogleScraper


def example_1_basic_usage():
    """Example 1: Basic usage - scrape all platforms."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60 + "\n")
    
    scraper = LeadScraper(max_results_per_platform=50)
    leads = scraper.scrape_all_platforms(filter_mec=True, min_engagement=0.5)
    
    print(f"\nTotal leads found: {len(leads)}")
    scraper.export_to_csv("example_basic_leads.csv")


def example_2_individual_platforms():
    """Example 2: Scrape individual platforms."""
    print("\n" + "=" * 60)
    print("Example 2: Individual Platform Scraping")
    print("=" * 60 + "\n")
    
    # Scrape only Instagram
    instagram = InstagramScraper(max_results=20)
    instagram_leads = instagram.get_leads(filter_mec=True, min_engagement=0.6)
    
    print(f"Instagram leads with high engagement (>0.6): {len(instagram_leads)}")
    for lead in instagram_leads[:3]:
        print(f"  - {lead.name}: {lead.engagement_score:.2f}")


def example_3_custom_filtering():
    """Example 3: Custom filtering and analysis."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Filtering")
    print("=" * 60 + "\n")
    
    scraper = LeadScraper(max_results_per_platform=50)
    
    # Get all leads without filtering
    all_leads = scraper.scrape_all_platforms(filter_mec=False, min_engagement=0.0)
    
    # Custom filtering
    high_engagement = [lead for lead in all_leads if lead.engagement_score > 0.8]
    high_followers = [lead for lead in all_leads if lead.followers > 30000]
    mentions_mec = [lead for lead in all_leads if lead.mentions_mec]
    
    print(f"Total leads: {len(all_leads)}")
    print(f"High engagement (>0.8): {len(high_engagement)}")
    print(f"High followers (>30k): {len(high_followers)}")
    print(f"Mentions MEC: {len(mentions_mec)}")


def example_4_platform_comparison():
    """Example 4: Compare platforms by engagement."""
    print("\n" + "=" * 60)
    print("Example 4: Platform Comparison")
    print("=" * 60 + "\n")
    
    scraper = LeadScraper(max_results_per_platform=50)
    leads = scraper.scrape_all_platforms(filter_mec=True, min_engagement=0.5)
    
    # Group by platform
    by_platform = {}
    for lead in leads:
        if lead.platform not in by_platform:
            by_platform[lead.platform] = []
        by_platform[lead.platform].append(lead)
    
    # Calculate average engagement per platform
    print("Platform Statistics:")
    for platform, platform_leads in by_platform.items():
        avg_engagement = sum(l.engagement_score for l in platform_leads) / len(platform_leads)
        avg_followers = sum(l.followers for l in platform_leads) / len(platform_leads)
        print(f"\n{platform}:")
        print(f"  Total leads: {len(platform_leads)}")
        print(f"  Avg engagement: {avg_engagement:.2f}")
        print(f"  Avg followers: {avg_followers:.0f}")


def example_5_export_formats():
    """Example 5: Different export formats."""
    print("\n" + "=" * 60)
    print("Example 5: Export to Multiple Formats")
    print("=" * 60 + "\n")
    
    scraper = LeadScraper(max_results_per_platform=50)
    scraper.scrape_all_platforms(filter_mec=True, min_engagement=0.5)
    
    # Export to both formats
    csv_file = scraper.export_to_csv("example_leads.csv")
    json_file = scraper.export_to_json("example_leads.json")
    
    print(f"\nExported to:")
    print(f"  CSV: {csv_file}")
    print(f"  JSON: {json_file}")


if __name__ == "__main__":
    print("\n🚀 Lead Scraper Examples\n")
    
    # Run all examples
    example_1_basic_usage()
    example_2_individual_platforms()
    example_3_custom_filtering()
    example_4_platform_comparison()
    example_5_export_formats()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60 + "\n")
