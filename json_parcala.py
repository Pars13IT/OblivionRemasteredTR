import json
import os
import argparse
from collections import OrderedDict

def split_json_file(input_filepath, output_directory, items_per_file):
    """
    Splits a large JSON file (specifically one with a single top-level key
    containing a dictionary of key-value pairs) into smaller JSON files,
    each containing a specified number of key-value pairs.

    Args:
        input_filepath (str): The path to the large input JSON file.
        output_directory (str): The directory where smaller JSON files will be saved.
        items_per_file (int): The maximum number of key-value pairs to include
                              in each output JSON file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            full_data = json.load(f, object_pairs_hook=OrderedDict) # Use OrderedDict to preserve key order
    except FileNotFoundError:
        print(f"Hata: '{input_filepath}' dosyası bulunamadı.")
        return
    except json.JSONDecodeError:
        print(f"Hata: '{input_filepath}' geçerli bir JSON dosyası değil.")
        return

    # Ensure the top-level is an object
    if not isinstance(full_data, dict):
        print("Hata: JSON dosyasının en üst düzeyde bir nesne olması bekleniyor.")
        return

    # We expect a single key at the top level
    if len(full_data) != 1:
        print("Hata: JSON dosyasının en üst düzeyde yalnızca bir anahtar içermesi bekleniyor.")
        return

    # Get the key and the inner object (e.g., "ST_ScriptContent" and its content)
    # Using next(iter(full_data.items())) to get the single key-value pair
    top_level_key, inner_value = next(iter(full_data.items()))

    if not isinstance(inner_value, dict):
        print(f"Hata: Anahtar '{top_level_key}' altındaki değerin bir nesne olması bekleniyor.")
        return

    # Get the inner dictionary of script content
    script_content = inner_value
    items = list(script_content.items()) # Get key-value pairs as a list of tuples
    # Python dictionaries retain insertion order from 3.7+, but list(items()) ensures it.
    # Sorting explicitly for deterministic output, similar to Rust's BTreeMap.
    items.sort(key=lambda x: x[0])

    total_items = len(items)
    print(f"Toplamda {total_items} öğe bulundu.")

    file_index = 0
    for i in range(0, total_items, items_per_file):
        file_index += 1
        chunk_items = items[i:i + items_per_file]

        # Reconstruct the inner dictionary for the chunk, preserving order
        chunk_dict = OrderedDict(chunk_items)

        # Wrap the chunk in the original top-level key structure
        output_data = OrderedDict()
        output_data[top_level_key] = chunk_dict

        # Create a unique filename for each part
        output_filename = os.path.join(output_directory, f"{top_level_key}_part_{file_index:03d}.json")

        try:
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                json.dump(output_data, outfile, ensure_ascii=False, indent=2)
            print(f"'{output_filename}' dosyası başarıyla oluşturuldu. İçerdiği öğe sayısı: {len(chunk_items)}")
        except IOError as e:
            print(f"Hata: '{output_filename}' dosyasına yazılırken sorun oluştu: {e}")

    print("İşlem tamamlandı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Büyük bir JSON dosyasını daha küçük, geçerli JSON dosyalarına ayırır."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Büyük giriş JSON dosyasının yolu"
    )
    parser.add_argument(
        "-m", "--max-lines",
        type=int,
        default=1000,
        help="Çıkış JSON dosyası başına maksimum anahtar-değer çifti sayısı (varsayılan: 1000)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="output_json_parts",
        help="Daha küçük JSON dosyaları için çıktı dizini (varsayılan: output_json_parts)"
    )

    args = parser.parse_args()

    print("Büyük JSON dosyası ayrıştırılıyor...")
    print(f"Giriş Dosyası: {args.input}")
    print(f"Dosya Başına Maksimum Satır: {args.max_lines}")
    print(f"Çıkış Dizini: {args.output_dir}")

    split_json_file(args.input, args.output_dir, args.max_lines)
