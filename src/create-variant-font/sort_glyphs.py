import os
import shutil
from collections import defaultdict


def group_files_by_glyph(input_dir):
    glyph_variants = defaultdict(list)
    for filename in os.listdir(input_dir):
        if filename.endswith(".svg"):
            parts = filename.split("_")
            if len(parts) >= 4:
                glyph_name = parts[0]
                glyph_variants[glyph_name].append(filename)
    return glyph_variants


def sort_and_organize_files(input_dir, output_dir, glyph_variants):
    for glyph_name, files in glyph_variants.items():
        sorted_files = sorted(files, key=lambda f: int(f.split("_")[1]))
        for n, file in enumerate(sorted_files, start=1):
            variant_folder = os.path.join(output_dir, f"variant_{n}")
            os.makedirs(variant_folder, exist_ok=True)
            original_path = os.path.join(input_dir, file)
            target_path = os.path.join(variant_folder, file)
            shutil.copy(original_path, target_path)


def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    glyph_variants = group_files_by_glyph(input_dir)
    sort_and_organize_files(input_dir, output_dir, glyph_variants)
    print(f"glyph variants sorted into: {output_dir}")


if __name__ == "__main__":
    input_directory = "data/glyph_svg"
    output_directory = "data/variant_svg"
    main(input_directory, output_directory)
