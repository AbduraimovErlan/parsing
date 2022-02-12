import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0"
}
# req = requests.get(url, headers=headers)
# src = req.text
# print(src)
#
# with open("index.html", "w") as file:
#     file.write(src)

# with open("index.html") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#
#     all_categories_dict[item_text] = item_href

with open("all_categories_dict.json") as file:
    all_categories = json.load(file)
# print(all_categories)

iteration_count = int(len(all_categories)) -1
count = 0
print(f"Всего итерация: {iteration_count}")

for category_name, category_href in all_categories.items():

    req = [",", " ", "-", "'"]
    for item in req:
        if item in category_name:
            category_name = category_name.relace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    scr = req.text

    with open(f"data/{count}_{category_name}.html", "w") as file:
        file.write(scr)

    with open(f"data/{count}_{category_name}.html") as file:
        scr = file.read()

    soup = BeautifulSoup(scr, "lxml")

# проверка страница на наличие таблица с  продуктами

    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates,
            )
        )


        product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

        product_info = []
        for item in product_data:
            product_tds = item.find_all("td")

            title = product_tds[0].find("a").text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text

            product_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates,
                }
            )

            with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}, {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итерация: {iteration_count}")
    sleep(random.randrange(2, 4))