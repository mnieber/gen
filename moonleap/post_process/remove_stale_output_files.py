import os


def remove_stale_output_files(output_filenames, output_dir):
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            stage_file_path = os.path.abspath(os.path.join(root, file))
            if stage_file_path not in output_filenames:
                os.remove(stage_file_path)
