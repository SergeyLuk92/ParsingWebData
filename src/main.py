from src.core.crawler import WebSiteCrawler
import asyncio


if __name__ == "__main__":
    crawler = WebSiteCrawler()
    asyncio.run(crawler.main())