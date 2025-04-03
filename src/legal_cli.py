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
        categories = assistant._identify_relevant_categories(situation)
        expanded_categories = assistant._expand_categories(categories)
        
        # Analyze the situation and get results
        result = assistant.analyze_situation(situation)
        
        # Print results
        print("\nRelevant categories:", ', '.join(result['relevant_categories']))
        print("\nRelevant laws:")
        for law_name in result['relevant_laws']:
            print(f"- {law_name}")
        
        # Print advice
        print("\nAdvice:")
        print(result['advice'])
        
        if args.verbose:
            print("\nDetailed References:")
            for ref in result['references']:
                print(f"\n{ref['name_of_law']} ({ref['citation_title']})")
                print(f"  BWB ID: {ref['identification_number']}")
                print(f"  Domain: {ref['legal_domain']}")
                print(f"  Entry into force: {ref['date_of_entry_into_force']}")
                print(f"  Regulatory authority: {ref['regulatory_authority']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 