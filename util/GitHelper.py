import subprocess
import os
from datetime import date


class GitHelper:
    """Helper class for automating git operations on the weather-game repository"""

    @staticmethod
    def commit_and_push(repo_path, files_to_add, commit_date):
        """
        Commits and pushes files to the specified git repository.

        Args:
            repo_path: Path to the git repository
            files_to_add: List of file paths (relative to repo) to add
            commit_date: Date object or string for the commit message

        Returns:
            True if successful, False otherwise
        """
        # Convert date to string if needed
        if isinstance(commit_date, date):
            date_str = commit_date.strftime('%Y-%m-%d')
        else:
            date_str = str(commit_date)

        commit_message = f"Add data for {date_str}"

        try:
            # Check if the repo path exists
            if not os.path.exists(repo_path):
                print(f"Error: Repository path does not exist: {repo_path}")
                return False

            # Check if it's a git repository
            git_dir = os.path.join(repo_path, '.git')
            if not os.path.exists(git_dir):
                print(f"Error: Not a git repository: {repo_path}")
                return False

            print(f"Committing to repository: {repo_path}")

            # Add files
            for file in files_to_add:
                file_path = os.path.join(repo_path, file)
                if os.path.exists(file_path):
                    result = subprocess.run(
                        ['git', 'add', file],
                        cwd=repo_path,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"Error adding file {file}: {result.stderr}")
                        return False
                    print(f"Added: {file}")
                else:
                    print(f"Warning: File does not exist: {file_path}")

            # Check if there are changes to commit
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if not status_result.stdout.strip():
                print("No changes to commit")
                return True

            # Commit
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if commit_result.returncode != 0:
                print(f"Error committing:")
                print(f"  Return code: {commit_result.returncode}")
                print(f"  stderr: {commit_result.stderr}")
                print(f"  stdout: {commit_result.stdout}")
                return False

            print(f"Committed: {commit_message}")

            # Push
            push_result = subprocess.run(
                ['git', 'push'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if push_result.returncode != 0:
                print(f"Error pushing: {push_result.stderr}")
                return False

            print("Pushed to remote successfully")
            return True

        except subprocess.TimeoutExpired:
            print("Error: Git push timed out")
            return False
        except Exception as e:
            print(f"Error during git operations: {e}")
            return False
