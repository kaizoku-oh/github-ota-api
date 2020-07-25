# Github OTA API
![GitHub release](https://img.shields.io/github/v/release/kaizoku-oh/github-ota-api)
![GitHub issues](https://img.shields.io/github/issues/kaizoku-oh/github-ota-api)
![GitHub top language](https://img.shields.io/github/languages/top/kaizoku-oh/github-ota-api)
![Flask version](https://img.shields.io/github/pipenv/locked/dependency-version/kaizoku-oh/github-ota-api/flask)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Serving binary release asset from GitHub to devices.

![Twitter follow](https://img.shields.io/twitter/follow/kaizoku_ouh?style=social)

# github-ota-api

**Base URL:** https://github-ota-api.herokuapp.com

**Endpoint:** /firmware/latest

### Request example:
```http
GET http://github-ota-api.herokuapp.com/firmware/latest?github_username=kaizoku-oh&github_repository=pio-freertos&device_current_fw_version=1.4.0
```
### Response example:
```json
{
  "download_url": "https://github-production-release-asset-2e65be.s3.amazonaws.com/208622543/e4888800-96c8-11ea-9a9e-5c47f103310b?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20200725%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20200725T153508Z&X-Amz-Expires=300&X-Amz-Signature=be26eaa701d4dbe47cca57e8a01e31a2f36d045beaef3a0c1311bde8e1fd94d5&X-Amz-SignedHeaders=host&actor_id=0&repo_id=208622543&response-content-disposition=attachment%3B%20filename%3Dfirmware.bin&response-content-type=application%2Foctet-stream",
  "version": "1.7.0"
}
```

## Deployment notes:
It's recommended to keep your github repo changes aligned with the heroku repo by following these steps.
### 1. Push code to GitHub
```bash
$ git clone https://github.com/kaizoku-oh/github-ota-api
$ cd github-ota-api
$ git checkout dev
# make your changes to the code
$ git add .
$ git commit -m "your commit message here"
$ git push origin dev
# Go to Github, open a pull request and merge merge changes
$ git checkout master
$ git pull
```
### 2. Push code to Heroku
```bash
$ heroku login
# Add a heroku remote to your local repository
$ heroku git:remote -a github-ota-api
$ git push heroku master
```