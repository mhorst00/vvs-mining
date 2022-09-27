import json
import vvspy
import sys

trip = vvspy.get_trip("de:08111:6052", "de:08111:6118").raw


trip.pop("fare")
trip.pop("rating")
trip.pop("isAdditional")
trip.pop("daysOfService")
for i in range(len(trip["legs"])):
    trip["legs"][i].pop("coords")
print(trip["legs"][0].keys())
# print(json.dumps(trip, indent=2))
print(sys.getsizeof(trip))
