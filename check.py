import requests


# default headers used in every request
HEADERS = {
    # fake user agent
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
}

"""
Individual website checker functions below.

These functions take no arguments and return a tuple in the form (bool, str/None),
meaning (appointment_found, message).

Different combinations of these return values mean different things:
(True, None) - Appointment was found, no additional message to display
(True, "some message") - Appointment was found, and this additional message should also be printed
(False, None) - No appointments found, and no errors
(False, "some error message") - An error was encountered while checking the website
"""

def cvs_checker():
    headers = HEADERS.copy()
    headers['Referer'] = 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine'

    response = requests.get('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.OR.json?vaccineinfo',
                            headers=headers)

    if response.status_code != 200:
        return False, response.text

    try:
        response_data = response.json()
    except:
        return False, response.text

    # CVS returns a list of all stores in the state
    locations_with_open_appointments = []
    for location in response_data['responsePayloadData']['data']['OR']:
        if location['status'] != "Fully Booked":
            locations_with_open_appointments.append(location['city'])

    if len(locations_with_open_appointments) > 0:
        return True, f"in cities: {', '.join(locations_with_open_appointments)}"

    return False, None


def walgreens_checker():
    headers = HEADERS.copy()
    headers['Cookie'] = 'XSRF-TOKEN=3dTXUizE6qFI4Q==.PLpVdjEKcs6ArMc6daNBi0MLhNS8e6LPA/JweSl2jwA=;'
    headers['X-XSRF-TOKEN'] = 'x9h6Tk4KNsEHpQ==.UOFWqFO7to4JGtgWZUn3XiVLirbRjrhvhZloG3cI10c='
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json, text/plain, */*'

    post_data = {"serviceId":"99","position":{"latitude":45.4923824,"longitude":-122.8029665},"appointmentAvailability":{"startDateTime":"2021-04-19"},"radius":25}

    response = requests.post('https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability',
                             headers=headers, json=post_data)

    if response.status_code != 200:
        return False, response.text

    try:
        response_data = response.json()
    except:
        return False, response.text

    if response_data['appointmentsAvailable']:
        return True, None

    return False, None


stores = {
    'CVS': cvs_checker,
    'Walgreens': walgreens_checker,
}

for store, check_function in stores.items():
    appointment_found, message = check_function()

    if appointment_found:
        print(f"Appointments available at {store}!")
        if message:
            print(message)

        continue

    if message is not None:
        print(f"ERROR - {store} - {error_message}")
        continue


