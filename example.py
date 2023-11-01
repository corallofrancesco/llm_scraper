from llm_scraper import ScraperAgent


if __name__ == "__main__":
    # TODO CLI

    agent = ScraperAgent(browser="firefox")

    website = "https://www.eurosport.it/basket/serie-a-basket/classifica.shtml"
    agent.scrape_website(website)

    question = "What is the first team listed?"
    answer = agent.answer(question)

    print(answer)
