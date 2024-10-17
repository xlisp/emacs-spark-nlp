import subprocess

def get_git_log():
    try:
        # Run the git log command
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%s"],
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

