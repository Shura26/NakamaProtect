import cloudscraper, json


#obtient un token d'access auprès du serveur de crunchyroll pour pouvoir requeter le serveur plus tard
def get_access_token():
    data = {
        "grant_type" : "client_id"
    }
    headers = {
        "Authorization": "Basic Y3Jfd2ViOg==",
    }

    scraper = cloudscraper.create_scraper()  
    response = scraper.post("https://www.crunchyroll.com/auth/v1/token", data=data, headers=headers).text
    json_data = json.loads(response)

    return json_data.get("access_token")



#récupère les 100 derniers id d'anime ajoutés
def get_lastest_anime_ids(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    scraper = cloudscraper.create_scraper()  
    response = scraper.get(f"https://www.crunchyroll.com/content/v2/discover/browse?n=100&sort_by=newly_added&ratings=true&locale=fr-FR", headers=headers).text
    json_data = json.loads(response)
    ids = []

    for item in json_data.get("data"):
        anime_id = item.get("id", None)
        
        if anime_id:
            ids.append(anime_id)

    return ids



#récupère tous les usernames qui ont postés des commentaires sur un anime
def get_usernames_from_comments(id_anime, token):

    headers = {
        "Authorization": f"Bearer {token}",
    }

    scraper = cloudscraper.create_scraper()  
    page_size = 100
    usernames = []

    # Obtenez le nombre total de commentaires
    response = scraper.get(f"https://www.crunchyroll.com/content-reviews/v2/fr-FR/review/series/{id_anime}/list?page=1&page_size=100&sort=helpful", headers=headers).text
    json_data = json.loads(response)
    total_comments = json_data.get("total", 0)

    if total_comments > 100:
        # Obtenez tous les commentaires de manière itérative
        for page in range(1, (total_comments // page_size) + 2):
            response = scraper.get(f"https://www.crunchyroll.com/content-reviews/v2/fr-FR/review/series/{id_anime}/list?page={page}&page_size={page_size}&sort=helpful", headers=headers).text
            json_data = json.loads(response)

            # Extraire les noms d'utilisateur
            for item in json_data.get("items", []):
                username = item.get("author", {}).get("username", None)
                
                if username:
                    usernames.append(username)
    else:
        # Extraire les noms d'utilisateur
        for item in json_data.get("items", []):
            username = item.get("author", {}).get("username", None)
                
            if username:
                usernames.append(username)

    return usernames


token = get_access_token()
anime_ids = get_lastest_anime_ids(token)

usernames_scraped = 0
for anime_id in anime_ids:
    users = get_usernames_from_comments(anime_id, token)
    usernames_scraped += len(users)
    print(usernames_scraped)
    #print(users)