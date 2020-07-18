import requests

FILE_URL = "https://github.com/kaizoku-oh/pio-esp32-https-ota/releases/download/v0.0.0/firmware.bin"

def main():
  response = requests.get(FILE_URL)
  print(response)
  if response.history:
    print("Request was redirected")
    if response.status_code == 200:
      print("Final destination:")
      print(response.status_code, response.url)
  else:
    print("Request was not redirected")

if __name__ == "__main__":
  main()