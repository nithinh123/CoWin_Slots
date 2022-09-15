import requests
import datetime
from win10toast import ToastNotifier
from playsound import playsound

class get_vaccine_slots():
    def get_slots(self,age,districts):
        given_date = self.get_dates()
        list = []
        header = {"accept": "application/json","Accept-Language": "hi_IN"}
        file_object = open('CowinWin.txt', 'a')
        result = ""
        for i in districts:
            for j in given_date:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={0}&date={1}".format(i,j)
                try:
                    result = requests.get(URL, headers=header)
                    if result.status_code != 200:
                        list = "Failed to fetch details from API:"+str(result.status_code)+"    "+str(datetime.datetime.now())
                        file_object.write("\n"+list)
                        return list
                except Exception as e:
                    list = "Failed to fetch details from API(Exception):"+str(e)+"    "+str(datetime.datetime.now())
                    file_object.write("\n"+list)
                    return list
                response_json = result.json()
                if response_json['sessions']:
                        for session in response_json['sessions']:
                            if session['min_age_limit']==age and session['available_capacity'] > 0 and session['available_capacity_dose1'] > 0:
                                list.append("Center:"+session["name"]+"."+"Pincode:"+str(session['pincode'])+"."+"Date:"+j+'.'+"Age:"+str(session['min_age_limit'])+"."+"Dose1:"+str(session['available_capacity_dose1'])+"."+"Dose2:"+str(session['available_capacity_dose2']))
        if len(list) > 0:
            toaster = ToastNotifier()
            toaster.show_toast(str(list))
            file_object.write("\n"+str(list)+str(datetime.datetime.now()))
            for i in range(5):
                print(list)
                playsound('slot.mp3')
                print("playing alert")
        else:
            file_object.write("\n"+"No slots found in Cowin Database    "+str(datetime.datetime.now()))
            print(list)

        file_object.close()
        return str(list)

    def get_dates(self):
        dt = datetime.date.today()
        days = 7
        dates = []
        for i in range(days):
            td = datetime.timedelta(days=i)
            date = dt + td
            dates.append(date.strftime("%d-%m-%Y"))
        return dates

age = 45
districts = [305]  #district codes
slot = get_vaccine_slots().get_slots(age,districts)
