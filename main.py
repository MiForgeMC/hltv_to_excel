import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

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

class team:
    def __init__(self, team_name, points, place, players, url):
        self.team_name = team_name
        self.points = points
        self.place = place
        self.players = players
        self.url = url

def get_player_info(url):
    responce = requests.get(url=f"https://www.hltv.org{url}", headers=fake_headers()).text
    bs4 = BeautifulSoup(responce, 'lxml')
    nickname = bs4.find("h1", class_="playerNickname").text
    name = bs4.find("div", class_="playerRealname").text[1:]
    country = bs4.find("img", class_="flag").get("title")
    age = bs4.find("div", class_="playerInfoRow playerAge").find("span", itemprop="text").text.replace(" years", '')
    return player(nickname, name, age, country, url)

responce = requests.get(url="https://www.hltv.org/ranking/teams/2024/february/5", headers=fake_headers()).text
bs4 = BeautifulSoup(responce, 'lxml')
teams = bs4.find_all("div", class_="ranked-team standard-box")
arr_teams = []

for team in teams:
    team_name = team.find("span", class_="name").text
    points = (team.find("span", class_="points").text[1:-1]).replace(" points", "")
    place = team.find("span", class_="position").text[1:]
    url = team.find("a", class_="moreLink").get("href")
    # players = list(map(lambda x: x.get("href"), team.find_all("a", class_="pointer")))
    # get_player_info(players[0])
    with ThreadPoolExecutor(max_workers=5) as executor:
        players = list(executor.map(get_player_info, list(map(lambda x: x.get("href"), team.find_all("a", class_="pointer")))))
    print(players)
    break



