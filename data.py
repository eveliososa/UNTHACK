import requests
import json

# HOLDS THE ENTIRE NAME OF THE AIRPORT
airport_list = [
    "LAX, Los Angeles International Airport, Los Angeles, CA",
    "ORD, Chicago O'Hare International Airport,Chicago,IL",
    "JFK, John F Kennedy International Airport, New York, NY",
    "DFW,Dallas Fort Worth International Airport,Dallas-Fort Worth,TX"
]

# HOLDS THE SYMBOL OF THE AIRPORT
symbol_list = []
for m in airport_list:
    symbol_list.append(m[0:3])

# HOLDS THE NUMBER OF AIRPORTS
num_of_airports = len(symbol_list)


# GETS DATA FOR FLIGHT SEARCH
def flights_search(date, origin, destination):
    all_flights = requests.get('https://unthackathon.herokuapp.com/flights?date=' + date + '&origin=' + origin +
                               '&destination='+destination)

    response_code = str(all_flights.status_code)
    if '2' == response_code[0]:
        all_flights_dict = json.loads(all_flights.text)

        flights = []
        for z in range(0, len(all_flights_dict)):
            flight = []

            # FLIGHT NUMBER
            flight_number = all_flights_dict[z]['flightNumber']
            flight.append(flight_number)

            # ORIGIN
            # code, city, timezone, latitude, longitude
            origin = []
            for x in all_flights_dict[z]['origin']:
                if x == 'location':
                    origin.append(all_flights_dict[z]['origin'][x]['latitude'])
                    origin.append(all_flights_dict[z]['origin'][x]['longitude'])
                else:
                    origin.append(all_flights_dict[z]['origin'][x])
            flight.append(origin)

            # DESTINATION
            # code, city, timezone, latitude, longitude
            destination = []
            for m in all_flights_dict[z]['destination']:
                if m == 'location':
                    destination.append(all_flights_dict[z]['destination'][m]['latitude'])
                    destination.append(all_flights_dict[z]['destination'][m]['longitude'])
                else:
                    destination.append(all_flights_dict[z]['destination'][m])
            flight.append(destination)

            # DISTANCE
            distance = all_flights_dict[z]['distance']
            flight.append(distance)

            # DURATION
            # hours, minutes
            duration = [all_flights_dict[z]['duration']['hours'], all_flights_dict[z]['duration']['minutes']]
            flight.append(duration)

            # DEPARTURE TIME
            dep_temp = time(all_flights_dict[z]['departureTime'][11:16])
            if dep_temp[0] == '0':
                dep_temp = dep_temp[1:len(dep_temp)]
            departure_time = dep_temp
            flight.append(departure_time)

            # ARRIVAL TIME
            dep_temp = time(all_flights_dict[z]['arrivalTime'][11:16])
            if dep_temp[0] == '0':
                dep_temp = dep_temp[1:len(dep_temp)]
            arrival_time = dep_temp
            flight.append(arrival_time)

            # AIRCRAFT
            # model, passenger total, passenger total main, passenger total first, speed
            aircraft = []
            for y in all_flights_dict[z]['aircraft']:
                if y == 'passengerCapacity':
                    aircraft.append(all_flights_dict[z]['aircraft'][y]['total'])
                    aircraft.append(all_flights_dict[z]['aircraft'][y]['main'])
                    aircraft.append(all_flights_dict[z]['aircraft'][y]['first'])
                else:
                    aircraft.append(all_flights_dict[z]['aircraft'][y])
            flight.append(aircraft)

            # append all flight info to flights list
            flights.append(flight)
        return flights
    else:
        return -1


# CONVERTS TIME
def time(time_in_min):
    hours, minutes = time_in_min.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "AM"
    if hours > 12:
        setting = "PM"
        hours -= 12
    temp = ("%02d:%02d" + setting) % (hours, minutes)
    return temp
