import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from xl import create_base_file, add_teams
from proxy import random_proxy
from io import BytesIO
from PIL import Image
import time

url = "https://www.hltv.org/ranking/teams/"

def fake_headers():
    ua = UserAgent()
    random_user_agent = ua.random
    headers = {'User-Agent': random_user_agent}
    return headers

class player:
    def __init__(self, nickname, name, age, country, url) -> None:
        self.nickname = nickname
        self.name = name
        self.age = age
        self.country = country
        self.url = url

class Team:
    def __init__(self, team_name, points, place, players, url, logo):
        self.team_name = team_name
        self.points = points
        self.place = place
        self.players = players
        self.logo = logo
        self.url = url

def get_player_info(url):
    while True:
        try:
            responce = requests.get(url=f"https://www.hltv.org{url}", headers=fake_headers(), proxies=random_proxy()).text
            bs4 = BeautifulSoup(responce, 'lxml')
            nickname = bs4.find("h1", class_="playerNickname").text
            name = bs4.find("div", class_="playerRealname").text[1:]
            country = bs4.find("img", class_="flag").get("title")
            age = bs4.find("div", class_="playerInfoRow playerAge").find("span", itemprop="text").text.replace(" years", '')
            return player(nickname, name, age, country, url)
        except Exception as err:
            print(f"Try again... Second request: {(str(err))}")
            time.sleep(1)

def get_image(url):
    while True:
        try:
            response = requests.get(url, headers=fake_headers(), proxies=random_proxy())
            img = BytesIO(response.content)
            Image.open(img)
            return img
        except Exception as err:
            print(f"Try again... Image request: {(str(err))}")
            time.sleep(1)

start = time.time()
while True:
    try:
        responce = requests.get(url=url, headers=fake_headers(), proxies=random_proxy()).text
        bs4 = BeautifulSoup(responce, 'lxml')
        # with open('output.html', 'w', encoding='utf-8') as file:
        #     file.write(str(bs4))
        teams = bs4.find_all("div", class_="ranked-team standard-box")
        actual_date = list(map(lambda x: x.text.replace(" ", ""), bs4.find_all("a", class_="sidebar-single-line-item selected")))
        arr_teams = []
        if teams != []:
            break
        print("Try again... Empty request")
    except Exception as err:
        print(f"Try again... First request: {(str(err))}")
        time.sleep(1)

for i, team in enumerate(teams):
    team_name = team.find("span", class_="name").text
    points = (team.find("span", class_="points").text[1:-1]).replace(" points", "")
    place = team.find("span", class_="position").text[1:]
    url = team.find("a", class_="moreLink").get("href")
    logo = get_image(team.find("span", class_="team-logo").find("img").get("src"))
    with ThreadPoolExecutor(max_workers=5) as executor:
        players = list(executor.map(get_player_info, list(map(lambda x: x.get("href"), team.find_all("a", class_="pointer")))))
    arr_teams.append(Team(team_name, points, place, players, url, logo))
    print(f"{i+1} team +")

create_base_file(actual_date)
add_teams(arr_teams, actual_date)
end = time.time()
total = end-start
print(f"Code execution time: {int(total // 3600)}:{int((total % 3600) // 60)}:{int(total % 60)}")