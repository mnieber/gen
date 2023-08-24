import filecmp
import os
import shutil

from moonleap.session import get_session

# Workflow:
#
# 1. Generate the output dir
# 2. Copy the output dir to the shadow dir
# 3. Compare the expected dir to the shadow dir
# 4. If you see something wrong in the shadow dir, fix the generator or spec
# 5. Regenerate the output dir using --smart.
#    The stage dir will contain the changes between output and shadow.
#    The sync_files function will tell you if the stage dir has new files compared to the shadow dir.
# 6. Compare the stage dir to the shadow dir.
#    If there are no new files, then disabled "New" in Meld.
#    Copy changes (which hopefully fix the mistakes) from stage to shadow. Verify in the diff between expected and shadow.

def sync_files(output_dir, shadow_dir, stage_dir):
    session = get_session()

    if not os.path.exists(shadow_dir):
        os.makedirs(shadow_dir)

    if not os.path.exists(stage_dir):
        os.makedirs(stage_dir)

    # Delete everything inside stage_dir
    for root, dirs, files in os.walk(stage_dir):
        for file in files:
            stage_file_path = os.path.join(root, file)
            os.remove(stage_file_path)
        for dir in dirs:
            stage_dir_path = os.path.join(root, dir)
            shutil.rmtree(stage_dir_path)

    # Sync files from output_dir to stage_dir. Any output files
    # that are identical to shadow files are not copied to stage.
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            output_file_path = os.path.join(root, file)
            shadow_file_path = os.path.join(
                shadow_dir, output_file_path[len(output_dir) + 1 :]
            )
            stage_file_path = os.path.join(
                stage_dir, output_file_path[len(output_dir) + 1 :]
            )
            stage_file_dir = os.path.dirname(stage_file_path)

            if not os.path.exists(shadow_file_path) or not filecmp.cmp(
                output_file_path, shadow_file_path
            ):
                os.makedirs(stage_file_dir, exist_ok=True)
                shutil.copy2(output_file_path, stage_file_path)

    # Create "Deleted" files in stage_dir for files in shadow_dir but
    # not in output_dir
    for root, dirs, files in os.walk(shadow_dir):
        for file in files:
            shadow_file_path = os.path.join(root, file)
            output_file_path = os.path.join(
                output_dir, shadow_file_path[len(shadow_dir) + 1 :]
            )
            stage_file_path = os.path.join(
                stage_dir, shadow_file_path[len(shadow_dir) + 1 :]
            )
            if not os.path.exists(output_file_path):
                os.makedirs(os.path.dirname(stage_file_path), exist_ok=True)
                with open(stage_file_path, "w") as f:
                    f.write("Deleted")

    # Count files in stage dir that are not in shadow_dir.
    for root, dirs, files in os.walk(stage_dir):
        for file in files:
            shadow_file_path = os.path.join(root, file)
            if not os.path.exists(shadow_file_path):
                session.report(f"New file: {file}")
