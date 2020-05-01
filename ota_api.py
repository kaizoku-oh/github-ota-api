import requests, semver
from flask import Flask, jsonify, request

GITHUB_USERNAME = 'kaizoku-619'
GITHUB_REPOSITORY = 'pio-ci-example'

# Define app using Flask
app = Flask(__name__)

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return 'Welcome to GitHub OTA API'

# Get download URL endpoint
@app.route('/getLatestReleaseUrl', methods=['GET'])
def get_latest_release_url():
    # TODO: Handle exception where argument is missing
    device_fw_version = request.args.get('version')
    board = request.args.get('board')
    ret, download_url = check_board_fw_version(device_fw_version, \
                                               board,             \
                                               GITHUB_USERNAME,   \
                                               GITHUB_REPOSITORY)
    if ret == True:
        return download_url
    else:
        # HTTP 204 No Content
        return '', 204

# Get URL of the latest firmware release binary
def check_board_fw_version(device_fw_version, board, github_user, github_repo):
    ret, download_url = False, ''

    response = requests.get('https://api.github.com/repos/{}/{}/releases/latest' \
                       .format(github_user, github_repo))                        \
                       .json()
    # TODO: Return without continuing function execution if the version is up-to-date
    server_fw_version = response['tag_name'][1:]
    assets = response['assets']

    for asset in assets:
        # examples: 'firmware_esp32dev.bin'
        #           'firmware_nodemcuv2.bin'
        if asset['name'] == 'firmware_{}.bin'.format(board):
            # if device_fw_version < server_fw_version
            if semver.compare(server_fw_version, device_fw_version) == 1:
                ret, download_url = True, asset['browser_download_url']
                break

    return ret, download_url

if __name__ == "__main__":
    # Run app on port 8080 in debug mode,
    # host='0.0.0.0' is used to make the app discoverable on LAN
    app.run(host='0.0.0.0', port=8080, debug=True)