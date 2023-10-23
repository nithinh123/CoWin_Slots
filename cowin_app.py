import requests
import datetime
from win10toast import ToastNotifier
from playsound import playsound


class GetVaccineSlots:
    def get_slots(self, age_group, district_list):
        given_date = self.get_dates
        data_list = []
        header = {"accept": "application/json", "Accept-Language": "hi_IN"}
        file_object = open('CowinWin.txt', 'a')
        base_url = "https://cdn-api.co-vin.in/api/v2/"
        for i in district_list:
            for j in given_date:
                url = base_url + f"appointment/sessions/public/findByDistrict?district_id={i}&date={j}"
                try:
                    result = requests.get(url, headers=header)
                    if result.status_code != 200:
                        data_list = "Failed to fetch details from API:" + str(result.status_code) + "    " + str(
                            datetime.datetime.now())
                        file_object.write("\n" + data_list)
                        return data_list
                except Exception as e:
                    data_list = "Failed to fetch details from API(Exception):" + str(e) + "    " + str(
                        datetime.datetime.now())
                    file_object.write("\n" + data_list)
                    return data_list
                response_json = result.json()
                print(response_json)
                if response_json['sessions']:
                    for session in response_json['sessions']:
                        if (session['min_age_limit'] == age_group and session['available_capacity'] > 0
                                and session['available_capacity_dose1'] > 0):
                            data_list.append("Center:" + session["name"] + "." + "Pincode:" + str(
                                session['pincode']) + "." + "Date:" + j + '.' + "Age:" + str(
                                session['min_age_limit']) + "." + "Dose1:" + str(
                                session['available_capacity_dose1']) + "." + "Dose2:" + str(
                                session['available_capacity_dose2']))
        if len(data_list) > 0:
            toaster = ToastNotifier()
            toaster.show_toast(str(data_list))
            file_object.write("\n" + str(data_list) + str(datetime.datetime.now()))
            for i in range(5):
                print(data_list)
                playsound('slot.mp3')
                print("playing alert")
        else:
            file_object.write("\n" + "No slots found in Cowin Database    " + str(datetime.datetime.now()))
            print(data_list)
        file_object.close()
        return str(data_list)

    @property
    def get_dates(self) -> list:
        dt = datetime.date.today()
        days = 7
        dates = []
        for i in range(days):
            td = datetime.timedelta(days=i)
            date = dt + td
            dates.append(date.strftime("%d-%m-%Y"))
        return dates


age = 45
district = [305]  # district codes
slot = GetVaccineSlots().get_slots(age, district)
