#!/usr/bin/env python3
"""
Challenge Creator: "only then does slaughter reveal its true form"

This script creates a forensics challenge file that demonstrates
the fragmented data analysis techniques described in the writeup.

Flag: SPL{brok3n_h3arts_and_fragment}
"""

import os
import random
import struct

def create_fragmented_challenge():
    """Create a binary file with fragmented flag data"""
    
    # The complete flag
    flag = "SPL{brok3n_h3arts_and_fragment}"
    
    # Split flag into fragments
    fragments = [
        "SPL{brok3n_h3",
        "arts_and_fragmen", 
        "t}"
    ]
    
    # Create binary data with fragments scattered throughout
    challenge_data = bytearray(4096)  # 4KB file
    
    # Fill with random-looking data (but not truly random for consistency)
    random.seed(42)  # Fixed seed for reproducibility
    for i in range(len(challenge_data)):
        challenge_data[i] = random.randint(0, 255)
    
    # Create clean positions for flag fragments (avoid overlap)
    positions = [
        (0x100, f"Heart FRAGMENT 1\n{fragments[0]}\x00"),
        (0x500, f"Heart FRAGMENT 2\n{fragments[1]}\x00"), 
        (0x900, f"Heart FRAGMENT 3\n{fragments[2]}\x00"),
    ]
    
    # Add some heart ASCII art for the theme
    heart_art = b"""
        ++       ++
      ++++       ++++
    ++++++       ++++++
  ++++++++       ++++++++
++++++++++       ++++++++++
 +++++++++++++++++++++++++++
  +++++++++++++++++++++++++
   +++++++++++++++++++++++
    +++++++++++++++++++++
     +++++++++++++++++++
      +++++++++++++++++
       +++++++++++++++
        +++++++++++++
         +++++++++++
          +++++++++
           +++++++
            +++++
             +++
              +
"""
    
    # Insert heart art at the beginning
    art_pos = 0x50
    for i, byte in enumerate(heart_art[:200]):  # Limit size
        if art_pos + i < len(challenge_data):
            challenge_data[art_pos + i] = byte
    
    # Insert fragments
    for pos, text in positions:
        data_bytes = text.encode()
        for i, byte in enumerate(data_bytes):
            if pos + i < len(challenge_data):
                challenge_data[pos + i] = byte
    
    # Add some red herrings (fake fragments) - move to safer positions
    red_herrings = [
        (0x200, "Heart FRAGMENT 0\nFAKE{not_the_flag}\x00"),
        (0x700, "Heart FRAGMENT 4\nCTF{wrong_format}\x00"),
        (0xB00, "Broken Heart Fragment\nSPL{fake_flag_here}\x00"),
    ]
    
    for pos, text in red_herrings:
        data_bytes = text.encode()
        for i, byte in enumerate(data_bytes):
            if pos + i < len(challenge_data):
                challenge_data[pos + i] = byte
    
    return bytes(challenge_data)

def create_metadata_file():
    """Create a metadata file with challenge information"""
    metadata = """# Challenge Metadata

## File Information
- **Filename**: broken_hearts.bin
- **Size**: 4096 bytes
- **Type**: Binary data with embedded fragments
- **Difficulty**: Intermediate

## Solution Hints
1. Look for "Heart FRAGMENT" markers
2. Extract data following each marker
3. Be careful of red herrings (fake fragments)
4. The correct fragments are numbered 1, 2, 3
5. Reassemble in order to get the complete flag

## Expected Flag
SPL{brok3n_h3arts_and_fragment}

## Analysis Commands
```bash
# Basic analysis
file broken_hearts.bin
xxd broken_hearts.bin | grep -i heart
strings broken_hearts.bin | grep -i fragment

# Fragment extraction
strings broken_hearts.bin | grep "Heart FRAGMENT [1-3]" -A 1

# Hex analysis of specific positions
xxd broken_hearts.bin | sed -n '17,20p'  # Fragment 1 area
xxd broken_hearts.bin | sed -n '81,84p'  # Fragment 2 area
xxd broken_hearts.bin | sed -n '145,148p' # Fragment 3 area
```
"""
    return metadata

def main():
    """Create the challenge files"""
    print("Creating forensics challenge: 'only then does slaughter reveal its true form'")
    
    # Create challenge binary
    challenge_data = create_fragmented_challenge()
    
    # Write challenge file
    with open("broken_hearts.bin", "wb") as f:
        f.write(challenge_data)
    print(f"✓ Created broken_hearts.bin ({len(challenge_data)} bytes)")
    
    # Create metadata
    metadata = create_metadata_file()
    with open("challenge_metadata.md", "w") as f:
        f.write(metadata)
    print("✓ Created challenge_metadata.md")
    
    # Verify the challenge works
    print("\n=== Challenge Verification ===")
    
    # Test extraction
    with open("broken_hearts.bin", "rb") as f:
        data = f.read()
    
    # Find fragments using strings approach
    fragments = {}
    
    # Convert to string for easier searching
    data_str = data.decode('utf-8', errors='ignore')
    
    # Look for fragment patterns
    import re
    pattern = r'Heart FRAGMENT ([1-3])\n(.+?)(?=\x00|\n|Heart|$)'
    matches = re.findall(pattern, data_str)
    
    for match in matches:
        frag_num = int(match[0])
        fragment_text = match[1].strip()
        fragments[frag_num] = fragment_text
    
    # Alternative method if regex doesn't work
    if not fragments:
        lines = data_str.split('\n')
        for i, line in enumerate(lines):
            if 'Heart FRAGMENT' in line and any(x in line for x in ['1', '2', '3']):
                if '1' in line:
                    frag_num = 1
                elif '2' in line: 
                    frag_num = 2
                elif '3' in line:
                    frag_num = 3
                else:
                    continue
                    
                # Get next line as fragment data
                if i + 1 < len(lines):
                    fragment_text = lines[i + 1].split('\x00')[0].strip()
                    if fragment_text:
                        fragments[frag_num] = fragment_text
    
    # Reconstruct flag
    if fragments:
        flag = ''.join(fragments[i] for i in sorted(fragments.keys()) if i in fragments)
        print(f"Extracted flag: {flag}")
        if flag == "SPL{brok3n_h3arts_and_fragment}":
            print("✓ Challenge verification successful!")
        else:
            print("⚠ Warning: Flag extraction may need adjustment")
    else:
        print("⚠ No fragments found during verification")
    
    print("\n=== Usage ===")
    print("1. Distribute 'broken_hearts.bin' as the challenge file")
    print("2. Use 'challenge_metadata.md' for reference (don't share with participants)")
    print("3. Expected solution process is documented in writeup.md")

if __name__ == "__main__":
    main()