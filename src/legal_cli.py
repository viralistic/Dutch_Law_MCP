#!/usr/bin/env python3
"""
Command-line interface for the Dutch Legal Assistant.
"""
import argparse
import sys
from src.test_legal_assistant import LegalAssistant

def main():
    parser = argparse.ArgumentParser(description='Dutch Legal Assistant - Get legal advice for your situation')
    parser.add_argument('situation', nargs='+', help='Describe your legal situation')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed information')
    
    args = parser.parse_args()
    
    # Join the situation words into a single string
    situation = ' '.join(args.situation)
    
    try:
        # Initialize the legal assistant
        assistant = LegalAssistant()
        
        # Analyze the situation
        print("\nAnalyzing your situation...")
        print("=" * 50)
        print(f"Situation: {situation}")
        print("=" * 50)
        
        # Get relevant categories and laws
        categories = assistant.identify_relevant_categories(situation)
        expanded_categories = assistant.expand_categories(categories)
        laws = assistant.fetch_relevant_laws(expanded_categories)
        
        # Print results
        print("\nRelevant categories:", ', '.join(expanded_categories))
        print("\nRelevant laws:")
        for law in laws:
            print(f"- {law.metadata['name_of_law']} ({law.metadata['citation_title']})")
        
        # Generate and print advice
        print("\nAdvice:")
        advice = assistant.generate_advice(situation, expanded_categories, laws)
        print(advice)
        
        if args.verbose:
            print("\nDetailed References:")
            for law in laws:
                print(f"\n{law.metadata['name_of_law']} ({law.metadata['citation_title']})")
                print(f"  BWB ID: {law.metadata['identification_number']}")
                print(f"  Domain: {law.metadata['legal_domain']}")
                print(f"  Entry into force: {law.metadata['date_of_entry_into_force']}")
                print(f"  Regulatory authority: {law.metadata['regulatory_authority']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 