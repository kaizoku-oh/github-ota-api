import requests

FILE_URL = "https://github.com/kaizoku-619/pio-ci-example/releases/download/v1.0.1/firmware_esp32dev.bin"

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