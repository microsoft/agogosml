#! /usr/bin/env bash

## assumes: TWINE_USERNAME, TWINE_PASSWORD, GITHUB_ACCESS_TOKEN are set as environment variables.
## requires pipenv, jq, curl and pipenv to be installed

echo "Do you want to bump major, minor or patch version?"
read versionbump

#AGOGOSML_VERSION="$(ls dist/agogosml_cli-*.tar.gz | egrep -o '[0-9].*[0-9]')"
AGOGOSML_VERSION=$(python ./agogosml/agogosml/__init__.py)

for i in agogosml*/ ; do
    cd $i
    pipenv install -r requirements-dev.txt && \
    pipenv install -r requirements.txt && \
        pipenv run make clean && \
        pipenv run make lint && \
        pipenv run make test &&  \
        pipenv run make coverage && \
        pipenv run make docs && \
        pipenv run bumpversion --current-version $AGOGOSML_VERSION $versionbump setup.py && \
        pipenv run make dist
        pipenv run make release
    cd ../
done

# Get New Version
AGOGOSML_VERSION=$(python ./agogosml/agogosml/__init__.py)

# Upload to GitHub Releases
CREATE_RELEASE_JSON="$(printf '{"tag_name":"%s", "name": "v%s"}\n' "$AGOGOSML_VERSION" "$AGOGOSML_VERSION")"
RESPONSE="$(curl -X POST \
    $(printf 'https://api.github.com/repos/Microsoft/agogosml/releases?access_token=%s' "$GITHUB_ACCESS_TOKEN") \
    -H 'Content-Type: application/json' \
    -d $CREATE_RELEASE_JSON)"
UPLOAD_URL="$(echo "$RESPONSE" | jq -r .upload_url | sed -e "s/{?name,label}//")"
curl -X POST -H 'Content-Type:application/gzip' \
    --data-binary "@$(ls agogosml_cli/dist/agogosml_cli-*.tar.gz)" \
    "$UPLOAD_URL?name=$(basename agogosml_cli/dist/agogosml_cli-*.tar.gz)&access_token=$GITHUB_ACCESS_TOKEN"
curl -X POST -H 'Content-Type:application/gzip' \
    --data-binary "@$(ls agogosml/dist/agogosml-*.tar.gz)" \
    "$UPLOAD_URL?name=$(basename agogosml/dist/agogosml-*.tar.gz)&access_token=$GITHUB_ACCESS_TOKEN"
