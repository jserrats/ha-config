import requests
from bs4 import BeautifulSoup

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "cron"


def setup(hass, config):
    smbc_entity_id_title = "cron.smbc_title"
    smbc_entity_id_image = "cron.smbc_image"

    ara_entity_id_title = "cron.ara_text"
    ara_entity_id_image = "cron.ara_image"

    def update_smbc(call):
        title, image = _get_last_comic()
        hass.states.set(smbc_entity_id_title, title)
        hass.states.set(smbc_entity_id_image, image)

    def update_ara(call):
        today_article = _get_last_article()
        title, body, picture = _extract_info_from_article(today_article)
        text = '*' + title + '*\n' + body
    #   hass.states.set(ara_entity_id_image, picture)
    #    hass.states.set(ara_entity_id_title, text)

    # initial state
    update_smbc(None)
    #update_ara(None)

    hass.services.register(DOMAIN, "update_smbc", update_smbc)
    #hass.services.register(DOMAIN, "update_ara", update_ara)

    # Return boolean to indicate that initialization was successfully.
    return True

def _get_last_comic():
    r = requests.get("https://www.smbc-comics.com/comic")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    img = soup.findAll("img")
    for i in img:
        try:
            if i["id"] == "cc-comic":
                return i["title"], i["src"]
        except KeyError:
            pass

def _get_last_article():
    r = requests.get('https://www.ara.cat/etiquetes/pareu_maquines.html')
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    article = soup.findAll("div", {'class': 'mt'})[0]
    soup1 = BeautifulSoup(str(article), "html.parser")
    info = soup1.findAll("a", {'class': 'lnk'})[0]
    if info['href'].startswith("https://"):
        return info['href']
    else:
        return "https://www.ara.cat" + info['href']


def _extract_info_from_article(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    title = soup.findAll('h1', {'class', 'pg-bkn-headline'})[0].text

    paragraphs = soup.findAll('p', {'class', 'mce'})
    body = '\n\n'.join([paragraph.text for paragraph in paragraphs])

    try:
        picture = soup.findAll('a', {'class', 'mg dummy lightbox'})[0]['href']
    except IndexError:
        picture = ""

    return title, body, picture