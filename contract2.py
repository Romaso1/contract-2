from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import logging


class WebScraper:
    """Абстракція веб-скрапера."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(by=locator[0], value=locator[1])

    def find_elements(self, locator):
        return self.driver.find_elements(by=locator[0], value=locator[1])

    def get_text(self, element):
        return element.text

    def click(self, element):
        element.click()


class NewsScraper(WebScraper):
    """Скрапер новинного сайту."""

    def __init__(self, driver):
        super().__init__(driver)

    def scrape_news(self):
        # Відкриваємо головну сторінку сайту новин.
        self.driver.get("https://www.bbc.com/ukrainian")

        # Знаходимо всі заголовки новин з класом bbc-8arhad.
        headlines = self.find_elements((By.CLASS_NAME, "bbc-8arhad"))

        # Збираємо дані про новини.
        news = []
        for headline in headlines:
            news.append({
                "title": headline.text,
                "url": headline.get_attribute("href"),
            })

        # Знаходимо всі описи новин з класом bbc-1kz5jpr.
        descriptions = self.find_elements((By.CLASS_NAME, "bbc-1kz5jpr"))

        # Додаємо описи до даних про новини.
        for news_item in news:
            if len(descriptions) > 0:
                news_item["description"] = descriptions.pop(0).text
            else:
                news_item["description"] = None

        return news


def main():
    # Ініціалізуємо драйвер браузера.
    driver = webdriver.Edge()

    # Створюємо скрапер новинного сайту.
    news_scraper = NewsScraper(driver)

    # Збираємо дані про новини.
    news = news_scraper.scrape_news()

    # Якщо новини були успішно зібрані, зберігаємо їх у файл.
    if news is not None:
        with open("news.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for n in news:
                writer.writerow([n["title"], n["url"], n["description"]])

        # Виводимо у консоль список новин, які будуть записані в файл.
        print("Новини, які будуть записані в файл:")
        for news_item in news:
            print(news_item)

    # Закриваємо драйвер браузера.
    driver.quit()


if __name__ == "__main__":
    main()
