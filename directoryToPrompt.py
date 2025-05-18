import os

def generate_directory_contents_file(base_dir, output_file, exclude_folders=None, exclude_files=None):
    if exclude_folders is None:
        exclude_folders = []
    if exclude_files is None:
        exclude_files = []

    # Add this script to excluded files
    current_script = os.path.basename(__file__)
    exclude_files.append(current_script)

    with open(output_file, 'w') as out_file:
        for root, dirs, files in os.walk(base_dir):
            # Normalize relative paths for exclusion checks
            rel_root = os.path.relpath(root, start=base_dir)

            # Remove excluded folders from the walk
            dirs[:] = [
                d for d in dirs
                if os.path.join(rel_root, d) not in [os.path.relpath(f, base_dir) for f in exclude_folders]
            ]

            for file in files:
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, base_dir)

                # Skip excluded files
                if any(ex_file in rel_file_path for ex_file in exclude_files):
                    continue

                # Write the file path as a section header
                out_file.write(f'{rel_file_path}:\n\n')

                # Write the file contents
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        out_file.write(f.read() + '\n')
                except Exception as e:
                    out_file.write(f'[ERROR READING FILE: {e}]\n')

                out_file.write('\n' + '-' * 80 + '\n')


if __name__ == '__main__':
    # Target directory and output file
    base_directory = '.'
    output_filename = 'dir_prompt.txt'

    # Exclusions (relative to base_directory)
    exclude_folders = ['node_modules', '.git']
    exclude_files = ['package-lock.json', 'package.json', '.gitignore', '.env.local']

    generate_directory_contents_file(base_directory, output_filename, exclude_folders, exclude_files)
    print(f"Directory contents written to {output_filename}")
