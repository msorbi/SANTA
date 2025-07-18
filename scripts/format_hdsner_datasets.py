#!/usr/bin/env python3
import argparse
import os
import json
import shutil

# def generate_meta_json(class_names):
#     """
#     Generates the content for meta.json, including entities and type2idx mapping.
#     Ensures 'PERS' precedes 'LOC' in type2idx.
#     """
#     entities = {}
#     type2idx = {"O": 0}
#     next_idx = 1

#     # Define the desired order for classes
#     ordered_classes = []
#     if "PERS" in class_names:
#         ordered_classes.append("PERS")
#     if "LOC" in class_names:
#         ordered_classes.append("LOC")
    
#     # Add any other classes found, sorted alphabetically, ensuring PERS and LOC are not duplicated
#     for other_class in sorted(c for c in class_names if c not in ["PERS", "LOC"]):
#         ordered_classes.append(other_class)

#     for class_name in ordered_classes:
#         entities[class_name] = {"short": class_name, "verbose": class_name}
#         type2idx[class_name] = next_idx
#         next_idx += 1
    
#     return {"entities": entities, "type2idx": type2idx}

def process_text_file_to_json(input_file_path, output_file_path):
    """
    Reads a source .txt file, parses it into sequences, extracts tokens and entities,
    and writes it to a .json file.
    """
    output_data = []
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by '\n\n' to get individual sequences/sentences
        sequences = content.strip().split('\n\n')
        
        for sequence in sequences:
            if not sequence.strip(): # Skip empty sequences
                continue
            
            tokens = []
            entities = []
            
            current_span_type = None
            current_span_start_idx = -1
            
            lines = sequence.strip().split('\n')
            for token_idx, line in enumerate(lines):
                parts = line.strip().split('\t')
                
                word = parts[0] if len(parts) > 0 else ""
                tag_str = parts[1] if len(parts) > 1 else "O" # Default to 'O' if tag is missing

                tokens.append(word)

                tag_prefix = tag_str.split('-')[0]
                tag_class = tag_str.split('-', 1)[1] if '-' in tag_str else None # Use split(..., 1) for safety

                # If a span is currently active
                if current_span_type is not None:
                    # If current token continues the span (I-tag with matching type)
                    if tag_prefix == "I" and tag_class == current_span_type:
                        # Continue the current span, no action needed on start/type
                        pass
                    else: # Current span ends (B-tag, O-tag, or I-tag with mismatch)
                        # Add the completed span to entities
                        entities.append((
                            current_span_start_idx,
                            token_idx-1, # end is exclusive
                            current_span_type
                        ))
                        # Reset span tracking
                        current_span_type = None
                        current_span_start_idx = -1
                        
                        # If the current tag starts a new span, initialize it
                        if tag_prefix == "B":
                            current_span_type = tag_class
                            current_span_start_idx = token_idx
                else: # No span is currently active
                    if tag_prefix == "B":
                        current_span_type = tag_class
                        current_span_start_idx = token_idx
                    # If tag is 'O' or malformed 'I' without a preceding 'B', do nothing (discard from entities)
            
            # After iterating through all tokens in the sequence, check for any open span
            if current_span_type is not None:
                entities.append((
                    current_span_start_idx,
                    len(tokens)-1, # end is inclusive
                    current_span_type
                ))

            if tokens: # Only add if there are actual tokens
                output_data.append({"sentence": json.dumps(tokens), "labeled entities": json.dumps(entities)})

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(output_data, outfile)
        
    except FileNotFoundError:
        print(f"Warning: Source file not found: {input_file_path}")
    except Exception as e:
        print(f"Error processing {input_file_path}: {e}")


def transform_data_to_ner_format(input_dir, output_dir, output_prefix, output_suffix):
    """
    Transforms the data from the input directory into the specified NER dataset format.
    """
    # Ensure the main output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each dataset (e.g., CBMA, CDBE, HOME)
    for dataset_name in os.listdir(input_dir):
        dataset_path = os.path.join(input_dir, dataset_name)
        if not os.path.isdir(dataset_path):
            continue # Skip non-directory items

        # Construct the output subdirectory name for the current dataset
        output_dataset_dir_name = f"{output_prefix}{dataset_name}{output_suffix}"
        output_dataset_path = os.path.join(output_dir, output_dataset_dir_name)
        os.makedirs(output_dataset_path, exist_ok=True) # Create the dataset-specific output directory

        multiclass_path = os.path.join(dataset_path, "MULTICLASS")
        if not os.path.isdir(multiclass_path):
            print(f"Warning: 'MULTICLASS' directory not found in '{dataset_path}'. Skipping dataset '{dataset_name}'.")
            continue

        # 1. Identify single classes in the current dataset
        current_dataset_single_classes = []
        for class_dir in os.listdir(dataset_path):
            if os.path.isdir(os.path.join(dataset_path, class_dir)) and class_dir != "MULTICLASS":
                current_dataset_single_classes.append(class_dir)
        
        # # 2. Generate and save meta.json
        # meta_json_content = generate_meta_json(current_dataset_single_classes)
        # meta_json_output_path = os.path.join(output_dataset_path, "meta.json")
        # with open(meta_json_output_path, 'w', encoding='utf-8') as f:
        #     json.dump(meta_json_content, f, indent=4, ensure_ascii=False)

        # 3. Process train.txt, val.txt, test.txt from MULTICLASS to JSON
        file_mappings = {
            "train.txt": "train",
            "val.txt": "dev", # Renamed to dev
            "test.txt": "test"
        }

        for src_txt_file, dest_json_filename in file_mappings.items():
            source_txt_path = os.path.join(multiclass_path, src_txt_file)
            output_json_path = os.path.join(output_dataset_path, f"{dest_json_filename}.json")
            output_txt_path = os.path.join(output_dataset_path, f"{dest_json_filename}.txt")
            
            shutil.copy(source_txt_path, output_txt_path)
            process_text_file_to_json(source_txt_path, output_json_path)




def main():
    parser = argparse.ArgumentParser(
        description="Copy and transform files from a source directory to a new output directory structure."
    )
    parser.add_argument(
        "--input-dir", 
        required=True, 
        help="Path to the source directory containing datasets (e.g., CBMA, CDBE)."
    )
    parser.add_argument(
        "--output-dir", 
        required=True, 
        help="Path to the destination directory where the transformed data will be saved."
    )
    parser.add_argument(
        "--output-prefix", 
        default="hdsner_", 
        help="Optional prefix string to add to output dataset directory names."
    )
    parser.add_argument(
        "--output-suffix", 
        default="", 
        help="Optional suffix string to add to output dataset directory names (e.g., '-distant')."
    )

    args = parser.parse_args()

    transform_data_to_ner_format(args.input_dir, args.output_dir, args.output_prefix, args.output_suffix)


if __name__ == "__main__":
    main()
