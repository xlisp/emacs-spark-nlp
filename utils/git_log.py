import subprocess
import os

def get_git_log(work_path):
    try:
        # Ensure the work path exists and is a directory
        if not os.path.isdir(work_path):
            raise FileNotFoundError(f"The path {work_path} is not a valid directory.")

        # Run the git log command
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%s"],
            cwd=work_path,
            capture_output=True,
            text=True,
            check=True
        )

        # Process the output into a list of tuples
        commits = [
            (line.split('|')[0], line.split('|')[1])
            for line in result.stdout.strip().split('\n')
        ]

        return commits

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []
