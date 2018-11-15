#!/usr/bin/env bash

#basic setttings
GH_USERNAME=AWegnerGithub

#advanced settings
GITHUB_OUTPUT_FOLDER=built_website
PELICAN_OUTPUT_FOLDER=output
TARGET_REPO=$GH_USERNAME/$GH_USERNAME.github.io.git


if [ "$TRAVIS" == "true" ]; then
    # Ensure Pull requests are not deployed
    if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
        echo "Successfully built pull request #$TRAVIS_PULL_REQUEST."
        exit 0
    fi

    echo "Deploying site to $TARGET_REPO."
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
fi


# Get the most recent commit message of most recent commit
p_dir=$(pwd)
cd ..
commitHash=$(git rev-parse HEAD)
commitMessage=$(git log -1 --pretty=%B)
cd $p_dir

# Get current site
git clone https://github.com/$TARGET_REPO $GITHUB_OUTPUT_FOLDER

#copy the new output
cd $GITHUB_OUTPUT_FOLDER
rsync -rv --exclude=.git ../$PELICAN_OUTPUT_FOLDER/* . --delete

git add -A .
echo -e "Changes:"
git status -s
echo -e "\n"

detailedMessage="Commit $commitHash pushed to GitHub by Travis build $TRAVIS_BUILD_NUMBER"
git commit -m "$commitMessage" -m "$detailedMessage"
git push -fq https://$GH_USERNAME:$GITHUB_API_KEY@github.com/$TARGET_REPO &>/dev/null || exit $?
echo -e "Deploy completed\n"
