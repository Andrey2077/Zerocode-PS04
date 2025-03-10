import random
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

WIKI_LINK = "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"


def proceeed_request():

    global browser

    link = None

    for element in browser.find_elements(By.TAG_NAME, "div"):
        element_class = element.get_attribute("class")
        if element_class == "mw-search-result-heading":
            link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
            break

    if link:
        browser.get(link)
        proceed_actions()
    else:
        print("Не нашлось подходящий статей")
        return

def proceed_actions(articles = None, paragraphs = None):
    global browser
    answer = input("Что делаем дальше? Доступные варианты: \n"
                   "1 - Листаем параграфы текущей статьи\n"
                   "2 - Переходим на одну из связанных статей\n"
                   "3 - Выход\n")

    if answer.strip() == "1":
        # Листаем параграфы
        if paragraphs == None:
            paragraphs = browser.find_elements(By.TAG_NAME, "p")
        paragraph = random.choice(paragraphs)
        browser.execute_script("arguments[0].scrollIntoView();", paragraph)
        time.sleep(3)
        proceed_actions(None, paragraphs)
    elif answer.strip() == "2":
        # Переходим на связанные страницы
        articles = []
        for element in browser.find_elements(By.TAG_NAME, "a"):
            link = element.get_attribute("href")
            articles.append(link)

        if articles:
            article_link = random.choice(articles)
            browser.get(article_link)
            time.sleep(3)
            proceed_actions(articles, None)
    else:
        print("Не верно выбран вариант действия")
        return
    # browser.getlink()




request = input("Введите текст запроса для поиска \n")
browser = webdriver.Chrome()

if request == "":
    print("Не корректно введен текст запроса")

else:
    try:
        browser.get(WIKI_LINK)
        assert "Википедия" in browser.title

        time.sleep(5)
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.send_keys(request.strip())
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        proceeed_request()

    except Exception as e:
        print(f"Произошла ошибка {e}")
