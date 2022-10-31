import sys
from pprint import pprint
from datetime import date, timedelta

from kofic import Kofic


class KisoKofic(Kofic):

    def __init__(self, key):
        super().__init__(key)

    def get_box_office_movie_list(self):
        yesterday = date.today() - timedelta(1)
        box_office = super().get_daily_box_office(yesterday.strftime('%Y%m%d'), '10')
        return box_office

    def get_specific_movie_info(self, movie_code):
        movie = super().get_movie_info(movie_code)
        movie = movie["movieInfoResult"]["movieInfo"]

        data = dict()
        data["titleKr"] = movie["movieNm"]
        data["titleEn"] = movie["movieNmEn"]
        data["runningTime"] = movie["showTm"]
        data["genres"] = [name["genreNm"] for name in movie["genres"]]
        data["nations"] = [nation["nationNm"] for nation in movie["nations"]]
        data["directors"] = [name["peopleNm"] for name in movie["directors"]]
        data["actors"] = [name["peopleNm"] for name in movie["actors"][:5]]
        data["watchGrade"] = movie['audits'][0]['watchGradeNm']

        return data

    def get_movie_list(self, item=5):

        movie_list = self.get_box_office_movie_list()
        movie_list = movie_list['boxOfficeResult']['dailyBoxOfficeList']

        return_movie_list = list()

        for movie in movie_list[:item]:
            movie_code = movie["movieCd"]
            return_movie_list.append(self.get_specific_movie_info(movie_code))

        return return_movie_list


class Utils:

    @staticmethod
    def get_input(message, trigger=True):
        answer = input(">>> " + message)

        if trigger and answer == "exit":
            sys.exit("프로그램이 종료되었습니다.")

        return answer

    @staticmethod
    def fprint(title, message, format=True):

        print("=" * 50)
        print(title.center(50 - len(title)))
        print("=" * 50)
        if format:
            pprint(message)
        else:
            print(message)
        print("=" * 50)


class MovieKiosk:

    def __init__(self, movie_data):
        self.__movie_data = movie_data
        self.custom_price_data = {"adults": 10000, "kids": 5000, "elder": 8000}

    @staticmethod
    def check_watch_grade(grade):

        if grade == "전체관람가":
            return 0
        elif grade == "12세이상관람가":
            return 12
        elif grade == "15세이상관람가":
            return 15
        elif grade == "청소년관람불가":
            return 18
        else:
            return -1

    def check_validation(self, title):

        for temp in self.__movie_data:
            if temp["titleKr"] == title.strip():
                return True, self.check_watch_grade(temp["watchGrade"])
        return False, False

    def set_price_and_count(self, total_price, people_count, type):

        people_count[type] += 1
        total_price += self.custom_price_data[type]

        return total_price, people_count

    def user_mode(self):

        Utils.fprint("상영중인 영화 정보", self.__movie_data)
        input_data = Utils.get_input("예매하실 영화의 이름을 입력하세요. ")
        validation, limited_age = self.check_validation(input_data)

        if validation:
            input_age = Utils.get_input("모든 관람자의 나이를 입력하여 주시기 바랍니다. 띄어쓰기로 구분하십시오. ")
            input_age = input_age.strip().split(" ")

            total_price = 0
            people_count = {"elder": 0, 'kids': 0, 'adults': 0}

            for age in input_age:
                if age.isdigit():
                    age = int(age)

                    if age >= limited_age:
                        if age > 65:
                            total_price, people_count = self.set_price_and_count(total_price, people_count, 'elder')
                        elif age > 18:
                            total_price, people_count = self.set_price_and_count(total_price, people_count, 'adults')
                        else:
                            total_price, people_count = self.set_price_and_count(total_price, people_count, 'kids')
                    else:
                        Utils.fprint("안내", "본 영화는 {}세 이상이 관람할 수 있습니다. {}세인 해당 인원을 제외합니다.".format(limited_age, age), False)
                        continue
                else:
                    Utils.fprint("안내", "잘못된 연령입니다. 처음부터 다시 시도하여 주세요.", False)
                    return

            Utils.fprint("예매 안내", "총 {}명이며, 결제금액은 {}원입니다.".format(sum(people_count.values()), total_price), False)
            input_answer = Utils.get_input("예매하시겠습니까? 예매를 하시려면 'Y'또는 'y'를 입력하십시오. ")

            if input_answer.upper() == "Y":
                data = {"영화명": input_data,
                        "성인": "{}명".format(people_count["adults"]),
                        "경로": "{}명".format(people_count["elder"]),
                        "아동": "{}명".format(people_count["kids"]),
                        "총원": "{}명".format(sum(people_count.values())),
                        "금액": "{}원".format(total_price)
                        }
                Utils.fprint("예매 영수증", data)
            else:
                Utils.fprint("안내", "취소되었습니다. 처음부터 다시 시도하여 주세요.", False)
                return
        else:
            Utils.fprint("안내", "잘못된 영화 이름입니다. 다시 확인하여 주세요.", False)
            return


if __name__ == '__main__':

    path = sys.argv

    kofic = KisoKofic('ce1a6376a2e65465fd32dab29e80ab27')
    kiosk = MovieKiosk(kofic.get_movie_list())

    while True:
        kiosk.user_mode()
