import requests


class Kofic:

    def __init__(self, key):
        self.key = key
        self.daily_box_office_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
        self.movie_info_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"

    def get_daily_box_office(self, targetDt, itemPerPage):
        params = {
            'key': self.key,
            'targetDt': str(targetDt),
            'itemPerPage': str(itemPerPage)
        }
        response = requests.get(self.daily_box_office_url, params=params)
        return response.json()

    def get_movie_info(self, movieCd):
        params = {
            'key': self.key,
            'movieCd': str(movieCd)
        }
        response = requests.get(self.movie_info_url, params=params)
        return response.json()
