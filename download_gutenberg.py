#!/usr/bin/env python3
"""
Script to download text files from Project Gutenberg
Usage: python download_gutenberg.py <book_id> <output_filename>
Example: python download_gutenberg.py 11 alice.txt
"""

import sys
import urllib.request
import re

def download_gutenberg_text(book_id, output_filename):
    """
    Download a book from Project Gutenberg and save it to a file.
    
    Args:
        book_id: The Project Gutenberg book ID
        output_filename: The filename to save the book to
    """
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    
    try:
        print(f"Downloading book {book_id} from {url}...")
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
        
        # Try to extract just the main content (remove Gutenberg headers/footers)
        # Look for common start/end markers
        start_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
        ]
        
        end_markers = [
            "*** END OF THIS PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "End of Project Gutenberg",
            "End of the Project Gutenberg",
        ]
        
        # Find the start of actual content
        start_pos = 0
        for marker in start_markers:
            pos = content.find(marker)
            if pos != -1:
                # Find the next newline after the marker
                start_pos = content.find('\n', pos) + 1
                break
        
        # Find the end of actual content
        end_pos = len(content)
        for marker in end_markers:
            pos = content.find(marker)
            if pos != -1:
                end_pos = pos
                break
        
        # Extract the main content
        if start_pos > 0 and start_pos < end_pos:
            content = content[start_pos:end_pos]
        
        # Clean up the content
        content = content.strip()
        
        # Save to file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Successfully downloaded to {output_filename}")
        print(f"  File size: {len(content)} characters")
        print(f"  Lines: {content.count('\n') + 1}")
        
        return True
        
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")
        print(f"  URL: {url}")
        print(f"  Try alternative URL formats:")
        print(f"  - https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt")
        return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python download_gutenberg.py <book_id> <output_filename>")
        print("\nExamples:")
        print("  python download_gutenberg.py 11 alice.txt        # Alice in Wonderland")
        print("  python download_gutenberg.py 1342 pride.txt       # Pride and Prejudice")
        print("  python download_gutenberg.py 84 frankenstein.txt  # Frankenstein")
        print("\nPopular Italian texts:")
        print("  python download_gutenberg.py 1000 divina.txt      # La Divina Commedia")
        print("  python download_gutenberg.py 7001 promessi.txt    # I Promessi Sposi")
        sys.exit(1)
    
    book_id = sys.argv[1]
    output_filename = sys.argv[2]
    
    success = download_gutenberg_text(book_id, output_filename)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
