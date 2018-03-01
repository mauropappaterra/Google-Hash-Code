# Google Hash Code
# Main.py
# Created by 'Too Young Too Simple' on 01 of March 2018.
#
# TEAM MEMBERS ARE:
# Albert Yang
# Lei You
# Mauro J. Pappaterra
# Miel Verkerken
#
import math

current_time = 0

class Ride:
    def __init__(self, x1,y1,x2,y2,starting_time,finish_time):
        self.pick_up = (x1,y1)
        self.drop_off = (x2,y2)
        self.starting_time = starting_time
        self.finish_time = finish_time

        self.points = distance(self.pick_up, self.drop_off)
        self.tolerance_time =  self.finish_time - self.points
        self.picked = False # ride has been assign to car

class Car:
    def __init__(self):
        self.x = 0 # position x
        self.y = 0 # position y

        self.nearby_rides = [i for i in range(N)]
        self.assigned_rides = [] # all rides assign to this car
        self.occupied = 0
        self.dropping_off = 0

    def __repr__(self):
        result = repr(len(self.assigned_rides)) + " "
        for index_ride in self.assigned_rides:
            result += repr(index_ride) + " "
        return result

def distance (a,b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def reward (car, ride):
    distance_pickup_car = distance(ride.pick_up,(car.x,car.y))
    bonus = 1 if distance_pickup_car <= (ride.starting_time - current_time) else 0
    validation = 0 if ride.finish_time >= distance_pickup_car + current_time + ride.points else 99999

    return ride.points + bonus * B - max(ride.starting_time - current_time, distance_pickup_car) - validation

# PATH TO INPUT
#path = "a_example.in"
#path = "b_should_be_easy.in"
#path = "c_no_hurry.in"
path = "d_metropolis.in"
#path = "e_high_bonus.in"

mode = "r"
with open (path, mode) as reader:
    all_input = (reader.readlines())
    reader.close()

configuration = all_input[0].split(' ') # save the first line of the file containing the configuration as a list of words
del all_input[0] # deletes the first line of the file, leaving only the rides
#print (configuration)

R = int(configuration[0]) # number of rows of the grid (1 ≤ R ≤ 10000)
C = int(configuration[1]) # number of columns of the grid (1 ≤ C ≤ 10000)
F = int(configuration[2]) # number of vehicles in the fleet (1 ≤ F ≤ 1000)
N = int(configuration[3]) # number of rides (1 ≤ N ≤ 10000)
B = int(configuration[4]) # per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
T = int(configuration[5]) # number of steps in the simulation (1 ≤ T ≤ 109)

# print("GIVEN CONFIGURATION:\nRows = " +  str(R) + "\nColumns = " +  str(C) +
#      "\nVehicles = " +  str(F) +  "\nRides = " +  str(N) +
#      "\nBonus Points = " + str(B) + "\nSteps = " + str(T))

all_rides = []
all_cars = []

for line in all_input:
    ride_info = [ int(i) for i in line.split(' ')]
    all_rides.append(Ride(ride_info[0],ride_info[1],ride_info[2],ride_info[3],ride_info[4],ride_info[5]))

for index_car in range(F):
    all_cars.append(Car())

for step in range(T):

    for car in all_cars:
        if not car.occupied:

            car.nearby_rides = sorted(car.nearby_rides, key=lambda index: -reward(car, all_rides[index]))

            i = 0
            while i < len(all_rides) and all_rides[car.nearby_rides[i]].picked:
                i += 1

            if not(i == len(all_rides)):
                current_ride = all_rides[car.nearby_rides[i]]
                car.assigned_rides.append(car.nearby_rides[i])
                car.occupied = current_ride.points + distance(current_ride.pick_up, (car.x, car.y))
                current_ride.picked = True

        if car.occupied:
            if not(car.dropping_off):
                if not(car.x == all_rides[car.assigned_rides[-1]].pick_up[0]):
                    car.x += 1 if all_rides[car.assigned_rides[-1]].pick_up[0] > car.x else -1
                elif not(car.y == all_rides[car.assigned_rides[-1]].pick_up[1]):
                    car.y += 1 if all_rides[car.assigned_rides[-1]].pick_up[1] > car.y else -1
                else:
                    car.dropping_off = True
            if car.dropping_off:
                if not(car.x == all_rides[car.assigned_rides[-1]].drop_off[0]):
                    car.x += 1 if all_rides[car.assigned_rides[-1]].drop_off[0] > car.x else -1
                elif not(car.y == all_rides[car.assigned_rides[-1]].drop_off[1]):
                    car.y += 1 if all_rides[car.assigned_rides[-1]].drop_off[1] > car.y else -1
                else:
                    car.dropping_off = False

        car.occupied -= 1

outFile = open("result_" + path, "w+")

for car in all_cars:
    outFile.write(repr(car) + "\n")

outFile.close()