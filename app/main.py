from flask import Flask, jsonify, request
import requests, semver

app = Flask(__name__)

# Root endpoint
@app.route("/", methods=["GET"])
def root_handler():
  return "Welcome to GitHub OTA API"

# Latest release download url endpoint
@app.route("/firmwares/latest", methods=["GET"])
def latest_release_url_handler():
  download_url = get_latest_release_url()
  if download_url:
    ret = {"download_url": download_url}
  else:
    # HTTP 204 No Content
    ret = "", 204
  return ret

def get_latest_release_url():
  download_url = ""
  # 1. Get parameters from device http request
  device_current_fw_version = request.args.get("device_current_fw_version")
  # board_variant = request.args.get("board")
  github_username = request.args.get("github_username")
  github_repository = request.args.get("github_repository")
  # 2. Build GitHub API URL
  github_api_url = "https://api.github.com/repos/{}/{}/releases/latest".format(github_username, github_repository)
  # 3. Send request to GitHub API and jsonify response
  json_response = requests.get(github_api_url).json()
  server_fw_version = json_response["tag_name"]
  # 4. if tag_name starts with "v" remove it, ex: "v1.0.1" ==> "1.0.1"
  if server_fw_version[0] == "v":
    server_fw_version = json_response["tag_name"][1:]
  # 5. Check versions semantic validity
  if semver.VersionInfo.isvalid(device_current_fw_version) and semver.VersionInfo.isvalid(server_fw_version):
    # 5.1. if device_current_fw_version < server_fw_version
    if semver.compare(server_fw_version, device_current_fw_version) == 1:
      # 5.2. extract browser download url from response
      assets = json_response["assets"]
      for asset in assets:
        if asset["name"] == "firmware.bin":
          browser_download_url = asset["browser_download_url"]
          break
      # 5.3. get the final download url
      response = requests.get(browser_download_url)
      # 5.4. if request was redirected get url
      if response.history:
        if response.status_code == 200:
          download_url = response.url
  return download_url
