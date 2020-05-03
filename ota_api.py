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
@app.route('/firmwares/latest', methods=['GET'])
def get_latest_release_url():
    device_fw_version = request.args.get('version')
    board = request.args.get('board')
    
    if device_fw_version and board:
        ret, download_url = check_board_fw_version(device_fw_version, \
                                                   board,             \
                                                   GITHUB_USERNAME,   \
                                                   GITHUB_REPOSITORY)
    else:
        if not device_fw_version:
            print('[ERROR] No version found')
        if not board:
            print('[ERROR] No board found')
        return '', 400

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
    server_fw_version = response['tag_name'][1:]
    if semver.VersionInfo.isvalid(device_fw_version) and \
       semver.VersionInfo.isvalid(server_fw_version):
        # if device_fw_version < server_fw_version
        if semver.compare(server_fw_version, device_fw_version) == 1:
            assets = response['assets']
            for asset in assets:
                # examples: 'firmware_esp32dev.bin'
                #           'firmware_nodemcuv2.bin'
                if asset['name'] == 'firmware_{}.bin'.format(board):
                    download_url = asset['browser_download_url']

                    print('download_url = {}'.format(download_url))
                    r = requests.get(download_url)
                    print(r)
                    if r.history:
                        print('Request was redirected')
                        resp = r.history[0]
                        if r.status_code == 200:
                            print('Final destination:')
                            print(r.status_code, r.url)
                            return True, r.url

    return ret, download_url

if __name__ == "__main__":
    # Run app on port 8080 in debug mode,
    # host='0.0.0.0' is used to make the app discoverable on LAN
    app.run(host='0.0.0.0', port=8080, debug=True)