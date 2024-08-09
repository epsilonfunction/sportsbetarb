# Fetch all remote branches
git fetch --all

# Loop through each remote branch
for branch in `git branch -r | grep -v '\->'`; do
    # Get the branch name without the remote part (e.g., 'origin/branch' -> 'branch')
    local_branch=${branch#origin/}

    # Create the local branch tracking the remote branch if it doesn't exist
    git branch --track $local_branch $branch 2>/dev/null

    # Checkout the branch
    git checkout $local_branch

    # Pull the latest changes
    git pull --rebase
done

# Switch back to the original branch (e.g., 'main')
git checkout main
