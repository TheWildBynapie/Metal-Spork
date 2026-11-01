import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

# python process_balibase.py -d /path/to/your/balibase/folder
# python process_balibase.py -d

def process_balibase_directory(directory_path):
    dir_path = Path(directory_path)
    
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: '{directory_path}' is not a valid directory.")
        return

    # 1. Rename any '.tfa' file to '.fasta'
    print("\n--- Step 1: Renaming .tfa files to .fasta ---")
    tfa_files = list(dir_path.glob("*.tfa"))
    if not tfa_files:
        print("No .tfa files found.")
    for tfa_file in tfa_files:
        fasta_file = tfa_file.with_suffix(".fasta")
        # Ensure we don't overwrite an existing file accidentally
        if fasta_file.exists():
            print(f"Skipping rename for {tfa_file.name}: {fasta_file.name} already exists.")
        else:
            tfa_file.rename(fasta_file)
            print(f"Renamed: {tfa_file.name} -> {fasta_file.name}")

    # 2. Parse XML reference files and create aligned FASTA files
    print("\n--- Step 2: Extracting alignments from XML files ---")
    xml_files = list(dir_path.glob("*.xml"))
    if not xml_files:
        print("No .xml files found.")
        return

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Extract all sequence names and sequence data elements matching BAliBASE structure
            seq_names = [elem.text.strip() for elem in root.findall('.//seq-name') if elem.text]
            seq_datas = [elem.text.strip() for elem in root.findall('.//seq-data') if elem.text]
            
            if not seq_names or not seq_datas:
                print(f"Skipping {xml_file.name}: No <seq-name> or <seq-data> tags found.")
                continue
                
            if len(seq_names) != len(seq_datas):
                print(f"Warning: Mismatch in {xml_file.name} (Found {len(seq_names)} names vs {len(seq_datas)} sequences).")
                continue

            # Save to an aligned FASTA file with an '_aligned.fasta' suffix 
            # to avoid name collisions with the unaligned sequences.
            output_fasta = dir_path / f"{xml_file.stem}_aligned.fasta"
            
            with open(output_fasta, "w", encoding="utf-8") as out_f:
                for name, data in zip(seq_names, seq_datas):
                    cap_name = name[0].upper() + name[1:] if name else name
                    out_f.write(f">{cap_name}\n{data}\n")
            
            print(f"Converted: {xml_file.name} -> {output_fasta.name}")

        except ET.ParseError:
            print(f"Error: Could not parse XML file {xml_file.name}. It might be malformed.")
        except Exception as e:
            print(f"Unexpected error processing {xml_file.name}: {e}")

    print("\nProcessing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process BAliBASE directory: rename .tfa files and convert XML reference alignments to FASTA.")
    parser.add_argument("-d", "--dir", required=True, help="Path to the directory containing the BAliBASE files")
    
    args = parser.parse_args()
    process_balibase_directory(args.dir)