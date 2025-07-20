def merge_files(file_list, result_name="result.txt"):
    files_info = []
    for file_name in file_list:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                files_info.append((file_name, len(lines), lines))

        except FileNotFoundError:
            print(f"File {file_name} not found. Continuing...")

    files_info.sort(key=lambda x: x[1])

    with open(result_name, 'w', encoding='utf-8') as result_file:
        for filename, line_count, content in files_info:
            result_file.write(f'Filename - {filename}\n')
            result_file.write(f'File lines - {line_count}\n')
            result_file.writelines(content)
            result_file.write('\n\n')

    print(f'Result file - "{result_name}" created.')

merge_files(['1.txt', '2.txt', '3.txt'])