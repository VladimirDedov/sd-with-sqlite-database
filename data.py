import datetime, random, sqlite3
import time


class Data:
    @staticmethod
    def __readTXT(name_file):
        file = open(name_file, "r", encoding="utf-8")
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        file.close()
        if line1 == "Интранет портал государственных органов":
            print('IPGошники забивают вручную!')
            exit()
        return line1, line2

    # return one record from array
    @classmethod
    def return_data(cls, request=False, gos_org=False):

        try:
            conn = sqlite3.connect('sd.db')
        except:
            print('Не удалось открыть БД!')
            time.sleep(5)
        cursor = conn.cursor()
        try:
            c=cursor.execute("""
            SELECT count(request) FROM sd
            """)
            count = c.fetchone()
            id = random.randint(1, count[0]+1)
        except:
            print('Не удалось посчитать количество строк в таблице sd')
        if request:
            try:
                req = cursor.execute(f"""
                    SELECT request FROM sd 
                    WHERE go_id = {id}
                """)
                record = req.fetchone()
            except:
                print('Не удалось выбрать запись из БД')
            cursor.close()
            return record[0]
        elif gos_org:
            try:
                req = cursor.execute(f"""
                    SELECT go, fio, e_mail FROM sd 
                    WHERE go_id = {id}
                """)
                record = req.fetchone()
            except:
                print('Не удалось выбрать запись из БД')
            cursor.close()
            return record[:]


    # overwrite the number of requests
    @staticmethod
    def __write_fileTXT(text_lines):
        with open("sd.txt", "w", encoding="utf-8") as file:
            for text in text_lines:
                file.write(text + "\n")

    # Add to end file month and number of requests
    @staticmethod
    def __write_to_end_fileTXT(month, count):
        with open("sd.txt", "a", encoding="utf-8") as file:
            file.write(month + "\n")
            file.write(count + "\n")

    # Filling in the file SD
    @classmethod
    def to_change_txt_sd(cls, count):
        text_lines = []
        date = datetime.date.today()
        with open("sd.txt", "r", encoding="utf-8") as file:
            for t in file.readlines():
                text_lines.append(t.rstrip())

        if cls.number_of_mouth[date.month] == text_lines[-2]:
            count = int(text_lines[-1]) + count
            text_lines[-1] = str(count)
            cls.__write_fileTXT(text_lines)
        else:
            cls.__write_to_end_fileTXT(cls.number_of_mouth[date.month], str(count))
        file.close()

    # Data set

    try:
        inf_sistem, person_name = __readTXT("informsystem.txt")
    except:
        print("Не удалось прочитать файл informsystem.txt")
    try:
        login, password = __readTXT("login.txt")
    except:
        print("Не удалось прочитать файл login.txt")

    XPATH = '/html/body/div[1]/div[2]/main/div[2]/div[2]/div[2]/div/div/'
    PATH = "C:\Python\SD\sd_with_bd_sql\chromedriver.exe"
    url = [
        "https://sd.nitec.kz/pages/UI.php",
        "https://sd.nitec.kz/pages/UI.php?operation=new&class=UserRequest&c%5Borg_id%5D=1&c%5Bmenu%5D=NewUserRequest"
    ]
    number_of_mouth = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь"
    }
