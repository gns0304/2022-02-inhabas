import sys
from pprint import pprint

path = sys.argv
movie_data = [{
                   "title": "영화1",
                   "running_time": 120,
                   "start_time": "오후 1시 15분",
                   "limited_age": 12,
                   "genre": "Comedy"
               }, {
                   "title": "영화2",
                   "running_time": 70,
                   "start_time": "오후 1시 35분",
                   "limited_age": 19,
                   "genre": "Action"
               }, {
                   "title": "영화3",
                   "running_time": 80,
                   "start_time": "오후 2시 00분",
                   "limited_age": 0,
                   "genre": "Comedy"
               }]

user_movie_data = list()

price_data = {"adult": 10000, "kids": 5000, "elder": 8000}


def get_input(message, trigger=True):

    answer = input(">>> " + message)

    if trigger and answer == "exit":
        sys.exit("프로그램이 종료되었습니다.")

    return answer


def fprint(title, message, format=True):

    print("=" * 50)
    print(title.center(50-len(title)))
    print("=" * 50)
    if format:
        pprint(message)
    else:
        print(message)
    print("=" * 50)


def check_validation(title):

    for temp in movie_data:
        if temp["title"] == title.strip():
            return True, temp["limited_age"]
    return False, False


if __name__ == '__main__':

    if len(path) > 1:
        if len(path) == 2 and path[1] == "admin":
            while True:
                movie_data = movie_data + user_movie_data
                fprint("저정된 영화 정보", movie_data)

                input_mode = get_input("입력을 원하시면 '입력'을 입력하십시오. ")
                if input_mode == "입력":
                    input_movie = get_input("영화명, 상영시간, 시작시간, 관람제한연령, 영화장르 순으로 띄어쓰기로 구분하여 데이터를 입력하십시오. ")
                    input_movie = input_movie.strip().split(" ")
                    temp_dict = {
                       "title": input_movie[0],
                       "running_time": int(input_movie[1]),
                       "start_time": input_movie[2],
                       "limited_age": int(input_movie[3]),
                       "genre": input_movie[4]
                    }
                    user_movie_data.append(temp_dict)
                    fprint("안내", "영화 {}이(가) 등록되었습니다.".format(temp_dict["title"]), False)

                else:
                    fprint("안내", "잘못된 입력입니다. 처음부터 다시 시도하여 주세요.", False)
                    continue
        else:
            print("Error")
    else:
        # USER MODE
        while True:
            movie_data = movie_data + user_movie_data
            fprint("상영중인 영화 정보", movie_data)
            input_data = get_input("예매하실 영화의 이름을 입력하세요.")
            validation, limited_age = check_validation(input_data)
            if validation:

                input_age = get_input("모든 관람자의 나이를 입력하여 주시기 바랍니다. 띄어쓰기로 구분하십시오.")
                input_age = input_age.strip().split(" ")

                total_price = 0

                elder = 0
                kids = 0
                adults = 0

                for age in input_age:
                    if age.isdigit():

                        if int(age) > limited_age:

                            if int(age) > 65:
                                elder = elder + 1
                                total_price = total_price + price_data["elder"]
                            elif int(age) > 18:
                                adults = adults + 1
                                total_price = total_price + price_data["adult"]
                            else:
                                kids = kids + 1
                                total_price = total_price + price_data["kids"]
                        else:
                            fprint("안내", "본 영화는 {}세 이상이 관람할 수 있습니다. {}세인 해당 인원을 제외합니다.".format(limited_age, age), False)
                            continue
                    else:
                        fprint("안내", "잘못된 연령입니다. 처음부터 다시 시도하여 주세요.", False)
                        continue

                fprint("예매 안내", "총 {}명이며, 결제금액은 {}원입니다.".format(elder + kids + adults, total_price), False)
                input_answer = get_input("예매하시겠습니까? 예매를 하시려면 'Y'또는 'y'를 입력하십시오.")

                if input_answer.upper() == "Y":
                    data = {"영화명": input_data,
                            "성인": "{}명".format(adults),
                            "경로": "{}명".format(elder),
                            "아동": "{}명".format(kids),
                            "총원": "{}명".format(adults + kids + elder),
                            "금액": "{}원".format(total_price)
                            }
                    fprint("예매 영수증", data)
                else:
                    fprint("안내", "취소되었습니다. 처음부터 다시 시도하여 주세요.", False)
                    continue

            else:
                fprint("안내", "잘못된 영화 이름입니다. 다시 확인하여 주세요.", False)
                continue





