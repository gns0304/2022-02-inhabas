import requests
import re
from bs4 import BeautifulSoup


class NaverMovieCrawler:

    def __init__(self):
        self.basic_url = "https://movie.naver.com/movie/bi/mi/basic.naver"
        self.point_url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver"

    def get_basic_movie_data(self, id):

        url = self.basic_url + "?code={}".format(str(id))
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        title_kr = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
        title = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > strong")["title"]
        genres = soup.select("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a")
        nation = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(2) > a").text
        running_time = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)").text
        directors = soup.select("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a")

        return {
            "title_kr": title_kr,
            "title": title,
            "director": [director.text for director in directors],
            "genre": [genre.text for genre in genres],
            "nation": nation,
            "running_time": int(re.findall(r"\d+", running_time)[0])
        }

    def get_point_list(self, id, page):

        comments = []

        for i in range(1, page + 1):

            url = self.point_url + "?code={}&page={}".format(str(id), str(i))
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            li_tags = soup.select("body > div > div > div.score_result > ul > li")

            for li in li_tags:

                if li.select("div.score_reple > p > span > span"):
                    comment = li.select_one("div.score_reple > p > span > span > a")["data-src"].strip()
                else:
                    comment = li.select("div.score_reple > p > span")[-1].text.strip()

                if comment:
                    comments.append(comment)

        return comments

test = NaverMovieCrawler()
print(test.get_basic_movie_data(219402))
print(test.get_point_list(219812, 2))