#!/usr/bin/env python3
"""
enrich_index_html.py
Injects the full dual-view Saddle Timeline Gantt component, In-App Trip Notes & AI Fine-Tuning Studio,
and 5-tab mobile bottom navigation into index.html for the Rockies and Mount Robson expedition.
"""

import sys
import os
import re
import json

# Add skill scripts directory to path to import generate_gantt_html
skill_scripts = r"C:\Users\Jamie\.agents\skills\moto-adv-expedition-master\scripts"
if skill_scripts not in sys.path:
    sys.path.insert(0, skill_scripts)

from generate_gantt_chart import generate_gantt_html

# Define the 18 days of detailed schedule data
days_data = [
    {
        "day": 1, "dist_km": 530.0, "dist_mi": 329.3, "date": "Day 1 (Sat, Jul 10)",
        "title": "Hanmer to Wawa via Lake Superior East", "hotel": "Wawa Motor Inn / Log Chalets",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 1 Leg 1: Hanmer to Blind River", "route": "Hwy 17 West", "dep": "07:30 AM", "arr": "09:45 AM", "km": 203.0, "mi": 126.1, "saddle": "2h 15m", "stop_dur": "20m", "activity": "Fuel + Coffee", "pri_gas": "Blind River Shell (91 V-Power)"},
            {"name": "Stage 1 Leg 2: Blind River to Sault Ste. Marie", "route": "Hwy 17 West", "dep": "10:05 AM", "arr": "11:45 AM", "km": 143.0, "mi": 88.9, "saddle": "1h 40m", "stop_dur": "40m", "activity": "Lunch + Gas", "pri_gas": "Sault Ste. Marie Esso (91 Octane)"},
            {"name": "Stage 1 Leg 3: Sault Ste. Marie to Old Woman Bay", "route": "Hwy 17 North Shore", "dep": "12:25 PM", "arr": "02:30 PM", "km": 105.0, "mi": 65.2, "saddle": "2h 05m", "stop_dur": "25m", "activity": "Old Woman Bay Red Cliffs Overlook", "pri_gas": "Pancake Bay"},
            {"name": "Stage 1 Leg 4: Old Woman Bay to Wawa", "route": "Hwy 17 North", "dep": "02:55 PM", "arr": "04:30 PM", "km": 79.0, "mi": 49.1, "saddle": "1h 35m", "stop_dur": "30m", "activity": "Giant Wawa Goose Photo + Check-in", "pri_gas": "Wawa Shell (91 V-Power)"}
        ],
        "arrival": "04:30 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 2, "dist_km": 480.0, "dist_mi": 298.3, "date": "Day 2 (Sun, Jul 11)",
        "title": "Wawa to Thunder Bay North Shore", "hotel": "Best Western Plus Nor'Wester",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 2 Leg 1: Wawa to White River", "route": "Hwy 17 North", "dep": "07:30 AM", "arr": "08:35 AM", "km": 90.0, "mi": 55.9, "saddle": "1h 05m", "stop_dur": "15m", "activity": "Winnie the Pooh Statue Photo", "pri_gas": "White River Esso"},
            {"name": "Stage 2 Leg 2: White River to Marathon", "route": "Hwy 17 West", "dep": "08:50 AM", "arr": "10:15 AM", "km": 100.0, "mi": 62.1, "saddle": "1h 25m", "stop_dur": "20m", "activity": "Fuel Top-off + Stretch", "pri_gas": "Marathon Petro-Canada (91 Octane)"},
            {"name": "Stage 2 Leg 3: Marathon to Terrace Bay & Nipigon", "route": "Hwy 17 Coastal Curves", "dep": "10:35 AM", "arr": "01:00 PM", "km": 174.0, "mi": 108.1, "saddle": "2h 25m", "stop_dur": "40m", "activity": "Lunch overlooking Terrace Bay Lighthouse", "pri_gas": "Nipigon Esso (91 Octane)"},
            {"name": "Stage 2 Leg 4: Nipigon to Terry Fox Lookout / Thunder Bay", "route": "Hwy 17 West", "dep": "01:40 PM", "arr": "03:30 PM", "km": 116.0, "mi": 72.1, "saddle": "1h 50m", "stop_dur": "30m", "activity": "Terry Fox Monument & Sleeping Giant Panorama", "pri_gas": "Thunder Bay Shell (91 V-Power)"}
        ],
        "arrival": "04:00 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 3, "dist_km": 490.0, "dist_mi": 304.5, "date": "Day 3 (Mon, Jul 12)",
        "title": "Thunder Bay to Kenora Boreal Shield", "hotel": "Clarion Lakeside Inn Kenora",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 3 Leg 1: Thunder Bay to Kakabeka Falls", "route": "Hwy 11/17 West", "dep": "07:30 AM", "arr": "08:05 AM", "km": 32.0, "mi": 19.9, "saddle": "0h 35m", "stop_dur": "30m", "activity": "Kakabeka Falls Gorge Walk", "pri_gas": "Kakabeka Falls"},
            {"name": "Stage 3 Leg 2: Kakabeka Falls to Ignace", "route": "Hwy 17 Shield", "dep": "08:35 AM", "arr": "11:15 AM", "km": 213.0, "mi": 132.4, "saddle": "2h 40m", "stop_dur": "35m", "activity": "Lunch + Fuel Stop", "pri_gas": "Ignace Shell (91 V-Power)"},
            {"name": "Stage 3 Leg 3: Ignace to Dryden", "route": "Hwy 17 West", "dep": "11:50 AM", "arr": "01:10 PM", "km": 108.0, "mi": 67.1, "saddle": "1h 20m", "stop_dur": "20m", "activity": "Fuel + Max the Moose Photo", "pri_gas": "Dryden Esso (91 Octane)"},
            {"name": "Stage 3 Leg 4: Dryden to Kenora / Lake of the Woods", "route": "Hwy 17 West", "dep": "01:30 PM", "arr": "03:45 PM", "km": 137.0, "mi": 85.1, "saddle": "2h 15m", "stop_dur": "30m", "activity": "Husky the Muskie + Hotel Check-in", "pri_gas": "Kenora Shell (91 V-Power)"}
        ],
        "arrival": "04:15 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 4, "dist_km": 675.0, "dist_mi": 419.4, "date": "Day 4 (Tue, Jul 13)",
        "title": "Kenora to Regina Prairie Express", "hotel": "Delta Hotels by Marriott Regina",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 4 Leg 1: Kenora to Winnipeg Perimeter Bypass", "route": "Trans-Canada Hwy 1", "dep": "07:30 AM", "arr": "09:45 AM", "km": 209.0, "mi": 129.9, "saddle": "2h 15m", "stop_dur": "20m", "activity": "Fuel + Manitoba Border Coffee", "pri_gas": "Winnipeg Petro-Canada (91 Octane)"},
            {"name": "Stage 4 Leg 2: Winnipeg to Portage la Prairie", "route": "Trans-Canada Hwy 1", "dep": "10:05 AM", "arr": "11:00 AM", "km": 88.0, "mi": 54.7, "saddle": "0h 55m", "stop_dur": "30m", "activity": "Early Lunch Stop", "pri_gas": "Portage Shell (91 V-Power)"},
            {"name": "Stage 4 Leg 3: Portage la Prairie to Brandon", "route": "Trans-Canada Hwy 1", "dep": "11:30 AM", "arr": "01:10 PM", "km": 133.0, "mi": 82.6, "saddle": "1h 40m", "stop_dur": "20m", "activity": "Fuel + Stretch", "pri_gas": "Brandon Esso (91 Octane)"},
            {"name": "Stage 4 Leg 4: Brandon to Indian Head & Regina", "route": "Trans-Canada Hwy 1", "dep": "01:30 PM", "arr": "04:45 PM", "km": 245.0, "mi": 152.2, "saddle": "3h 15m", "stop_dur": "20m", "activity": "Indian Head Statue + Fuel", "pri_gas": "Regina Delta Hub (91 Octane)"}
        ],
        "arrival": "05:05 PM", "supper": "06:45 - 07:45 PM"
    },
    {
        "day": 5, "dist_km": 465.0, "dist_mi": 288.9, "date": "Day 5 (Wed, Jul 14)",
        "title": "Regina to Medicine Hat Big Sky", "hotel": "Medicine Hat Lodge",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 5 Leg 1: Regina to Moose Jaw", "route": "Trans-Canada Hwy 1", "dep": "07:30 AM", "arr": "08:15 AM", "km": 72.0, "mi": 44.7, "saddle": "0h 45m", "stop_dur": "20m", "activity": "Mac the Moose World's Largest Moose Photo", "pri_gas": "Moose Jaw Shell"},
            {"name": "Stage 5 Leg 2: Moose Jaw to Swift Current", "route": "Trans-Canada Hwy 1", "dep": "08:35 AM", "arr": "10:45 AM", "km": 176.0, "mi": 109.4, "saddle": "2h 10m", "stop_dur": "35m", "activity": "Lunch + Fuel Stop", "pri_gas": "Swift Current Shell (91 V-Power)"},
            {"name": "Stage 5 Leg 3: Swift Current to Maple Creek", "route": "Trans-Canada Hwy 1", "dep": "11:20 AM", "arr": "01:10 PM", "km": 128.0, "mi": 79.5, "saddle": "1h 50m", "stop_dur": "20m", "activity": "Stretch + Cold Drinks", "pri_gas": "Maple Creek Co-op"},
            {"name": "Stage 5 Leg 4: Maple Creek to Medicine Hat", "route": "Trans-Canada Hwy 1", "dep": "01:30 PM", "arr": "02:45 PM", "km": 89.0, "mi": 55.3, "saddle": "1h 15m", "stop_dur": "30m", "activity": "Saamis Tepee (World's Tallest Tepee)", "pri_gas": "Medicine Hat Shell (91 V-Power)"}
        ],
        "arrival": "03:15 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 6, "dist_km": 390.0, "dist_mi": 242.3, "date": "Day 6 (Thu, Jul 15)",
        "title": "Medicine Hat to Canmore / Banff Gateway", "hotel": "Coast Canmore Hotel (Night 1 of 2)",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 6 Leg 1: Medicine Hat to Bassano", "route": "Trans-Canada Hwy 1", "dep": "07:30 AM", "arr": "09:30 AM", "km": 177.0, "mi": 110.0, "saddle": "2h 00m", "stop_dur": "20m", "activity": "Fuel + Morning Coffee", "pri_gas": "Bassano Esso (91 Octane)"},
            {"name": "Stage 6 Leg 2: Bassano to Calgary Stoney Trail", "route": "Trans-Canada Hwy 1", "dep": "09:50 AM", "arr": "11:30 AM", "km": 121.0, "mi": 75.2, "saddle": "1h 40m", "stop_dur": "40m", "activity": "Lunch west of Calgary", "pri_gas": "Calgary West Shell (91 V-Power)"},
            {"name": "Stage 6 Leg 3: Calgary to Canmore Mountain Wall", "route": "Hwy 1 Bow Valley", "dep": "12:10 PM", "arr": "01:30 PM", "km": 92.0, "mi": 57.2, "saddle": "1h 20m", "stop_dur": "30m", "activity": "Enter Rocky Mountains! Canmore Check-in", "pri_gas": "Canmore Shell (91 V-Power)"}
        ],
        "arrival": "02:00 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 7, "dist_km": 160.0, "dist_mi": 99.4, "date": "Day 7 (Fri, Jul 16)",
        "title": "Banff, Lake Louise & Yoho NP Loop", "hotel": "Coast Canmore Hotel (Night 2 of 2 - Luggage-Free!)",
        "wake": "07:30 AM", "rollout": "08:15 AM",
        "legs": [
            {"name": "Stage 7 Leg 1: Canmore to Castle Mountain via 1A", "route": "Bow Valley Parkway (1A)", "dep": "08:15 AM", "arr": "09:15 AM", "km": 56.0, "mi": 34.8, "saddle": "1h 00m", "stop_dur": "20m", "activity": "Castle Mountain Battlement Viewpoint", "pri_gas": "Lake Louise Shell"},
            {"name": "Stage 7 Leg 2: Castle Mountain to Lake Louise", "route": "Bow Valley Parkway", "dep": "09:35 AM", "arr": "10:15 AM", "km": 32.0, "mi": 19.9, "saddle": "0h 40m", "stop_dur": "45m", "activity": "Chateau Lake Louise & Victoria Glacier", "pri_gas": "Lake Louise Shell (91 Octane)"},
            {"name": "Stage 7 Leg 3: Lake Louise to Yoho NP (Spiral Tunnels & Emerald Lake)", "route": "Trans-Canada Hwy 1 West", "dep": "11:00 AM", "arr": "11:45 AM", "km": 36.0, "mi": 22.4, "saddle": "0h 45m", "stop_dur": "60m", "activity": "Lunch in Field + Emerald Lake Shoreline", "pri_gas": "Field BC"},
            {"name": "Stage 7 Leg 4: Emerald Lake return to Canmore", "route": "Trans-Canada Hwy 1 East", "dep": "12:45 PM", "arr": "02:00 PM", "km": 72.0, "mi": 44.7, "saddle": "1h 15m", "stop_dur": "20m", "activity": "Return to Canmore Basecamp", "pri_gas": "Canmore Shell (91 V-Power)"}
        ],
        "arrival": "02:20 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 8, "dist_km": 290.0, "dist_mi": 180.2, "date": "Day 8 (Sat, Jul 17)",
        "title": "Canmore to Jasper via ICEFIELDS PARKWAY", "hotel": "Forest Park Hotel Jasper (Night 1 of 2)",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 8 Leg 1: Canmore to Bow Lake & Peyto Lake", "route": "Icefields Parkway (Hwy 93N)", "dep": "07:30 AM", "arr": "09:15 AM", "km": 105.0, "mi": 65.2, "saddle": "1h 45m", "stop_dur": "45m", "activity": "Num-Ti-Jah Lodge + Peyto Lake Bow Summit (2,088m)", "pri_gas": "Saskatchewan Crossing"},
            {"name": "Stage 8 Leg 2: Peyto Lake to Saskatchewan River Crossing", "route": "Hwy 93N Weeping Wall", "dep": "10:00 AM", "arr": "10:50 AM", "km": 53.0, "mi": 32.9, "saddle": "0h 50m", "stop_dur": "25m", "activity": "MANDATORY MIDPOINT FUEL TOP-OFF", "pri_gas": "The Crossing Resort (91 Octane)"},
            {"name": "Stage 8 Leg 3: Saskatchewan Crossing to Columbia Icefield", "route": "Hwy 93N Sunwapta Pass", "dep": "11:15 AM", "arr": "12:15 PM", "km": 49.0, "mi": 30.4, "saddle": "1h 00m", "stop_dur": "60m", "activity": "Athabasca Glacier Toe Walk & Alpine Lunch", "pri_gas": "Icefield Centre"},
            {"name": "Stage 8 Leg 4: Columbia Icefield to Sunwapta & Athabasca Falls to Jasper", "route": "Hwy 93N Athabasca Valley", "dep": "01:15 PM", "arr": "03:15 PM", "km": 83.0, "mi": 51.6, "saddle": "2h 00m", "stop_dur": "30m", "activity": "Athabasca Falls Churn + Jasper Check-in", "pri_gas": "Jasper Petro-Canada (91 Octane)"}
        ],
        "arrival": "03:45 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 9, "dist_km": 210.0, "dist_mi": 130.5, "date": "Day 9 (Sun, Jul 18)",
        "title": "Jasper to MOUNT ROBSON (BC) Excursion", "hotel": "Forest Park Hotel Jasper (Night 2 of 2 - Luggage-Free!)",
        "wake": "07:30 AM", "rollout": "08:15 AM",
        "legs": [
            {"name": "Stage 9 Leg 1: Jasper to Yellowhead Pass Continental Divide", "route": "Yellowhead Hwy 16 West", "dep": "08:15 AM", "arr": "08:50 AM", "km": 36.0, "mi": 22.4, "saddle": "0h 35m", "stop_dur": "15m", "activity": "Continental Divide Alberta/BC Border Sign", "pri_gas": "Jasper"},
            {"name": "Stage 9 Leg 2: Yellowhead Pass to MOUNT ROBSON VISITOR CENTRE", "route": "BC Hwy 16 West", "dep": "09:05 AM", "arr": "09:55 AM", "km": 50.0, "mi": 31.1, "saddle": "0h 50m", "stop_dur": "45m", "activity": "EMPEROR FACE PANORAMA (3,954m Peak)", "pri_gas": "Mount Robson"},
            {"name": "Stage 9 Leg 3: Mount Robson to Berg Lake Trailhead & Overlander Falls", "route": "BC Hwy 16", "dep": "10:40 AM", "arr": "11:15 AM", "km": 19.0, "mi": 11.8, "saddle": "0h 35m", "stop_dur": "60m", "activity": "Berg Lake Moraine Overlook + Overlander Falls Walk", "pri_gas": "Valemount Shell"},
            {"name": "Stage 9 Leg 4: Mount Robson return to Jasper Basecamp", "route": "Yellowhead Hwy 16 East", "dep": "12:15 PM", "arr": "02:00 PM", "km": 105.0, "mi": 65.2, "saddle": "1h 45m", "stop_dur": "20m", "activity": "Relaxed Evening in Jasper Townsite", "pri_gas": "Jasper Petro-Canada (91 Octane)"}
        ],
        "arrival": "02:20 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 10, "dist_km": 365.0, "dist_mi": 226.8, "date": "Day 10 (Mon, Jul 19)",
        "title": "Jasper to Edmonton Athabasca Descent", "hotel": "Matrix Hotel Edmonton Downtown",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 10 Leg 1: Jasper to Hinton", "route": "Yellowhead Hwy 16 East", "dep": "07:30 AM", "arr": "08:35 AM", "km": 80.0, "mi": 49.7, "saddle": "1h 05m", "stop_dur": "20m", "activity": "Fuel + Morning Coffee", "pri_gas": "Hinton Shell (91 V-Power)"},
            {"name": "Stage 10 Leg 2: Hinton to Edson", "route": "Yellowhead Hwy 16", "dep": "08:55 AM", "arr": "10:10 AM", "km": 97.0, "mi": 60.3, "saddle": "1h 15m", "stop_dur": "20m", "activity": "Stretch + Snack", "pri_gas": "Edson Esso (91 Octane)"},
            {"name": "Stage 10 Leg 3: Edson to Evansburg", "route": "Yellowhead Hwy 16", "dep": "10:30 AM", "arr": "11:45 AM", "km": 89.0, "mi": 55.3, "saddle": "1h 15m", "stop_dur": "30m", "activity": "Lunch Stop", "pri_gas": "Evansburg Shell"},
            {"name": "Stage 10 Leg 4: Evansburg to Edmonton Downtown", "route": "Yellowhead Hwy 16 East", "dep": "12:15 PM", "arr": "01:45 PM", "km": 99.0, "mi": 61.5, "saddle": "1h 30m", "stop_dur": "20m", "activity": "Hotel Check-in & Downtown Walk", "pri_gas": "Edmonton Shell (91 V-Power)"}
        ],
        "arrival": "02:05 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 11, "dist_km": 525.0, "dist_mi": 326.2, "date": "Day 11 (Tue, Jul 20)",
        "title": "Edmonton to Saskatoon Parkland", "hotel": "Delta Hotels Bessborough",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 11 Leg 1: Edmonton to Vegreville", "route": "Yellowhead Hwy 16 East", "dep": "07:30 AM", "arr": "08:45 AM", "km": 105.0, "mi": 65.2, "saddle": "1h 15m", "stop_dur": "20m", "activity": "Giant Ukrainian Pysanka Easter Egg Photo", "pri_gas": "Vegreville Shell (91 V-Power)"},
            {"name": "Stage 11 Leg 2: Vegreville to Lloydminster Border City", "route": "Yellowhead Hwy 16", "dep": "09:05 AM", "arr": "10:50 AM", "km": 146.0, "mi": 90.7, "saddle": "1h 45m", "stop_dur": "35m", "activity": "Lunch on the Alberta/Sask Border", "pri_gas": "Lloydminster Petro-Canada (91 Octane)"},
            {"name": "Stage 11 Leg 3: Lloydminster to North Battleford", "route": "Yellowhead Hwy 16", "dep": "11:25 AM", "arr": "01:05 PM", "km": 132.0, "mi": 82.0, "saddle": "1h 40m", "stop_dur": "20m", "activity": "Fuel + Stretch", "pri_gas": "North Battleford Shell (91 V-Power)"},
            {"name": "Stage 11 Leg 4: North Battleford to Saskatoon", "route": "Yellowhead Hwy 16", "dep": "01:25 PM", "arr": "03:15 PM", "km": 142.0, "mi": 88.2, "saddle": "1h 50m", "stop_dur": "25m", "activity": "Bessborough Castle Hotel Check-in", "pri_gas": "Saskatoon Shell (91 V-Power)"}
        ],
        "arrival": "03:40 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 12, "dist_km": 540.0, "dist_mi": 335.5, "date": "Day 12 (Wed, Jul 21)",
        "title": "Saskatoon to Dauphin Riding Mountain", "hotel": "Super 8 by Wyndham Dauphin",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 12 Leg 1: Saskatoon to Wynyard", "route": "Yellowhead Hwy 16 East", "dep": "07:30 AM", "arr": "09:30 AM", "km": 169.0, "mi": 105.0, "saddle": "2h 00m", "stop_dur": "20m", "activity": "Fuel + Morning Coffee", "pri_gas": "Wynyard Esso (91 Octane)"},
            {"name": "Stage 12 Leg 2: Wynyard to Yorkton", "route": "Yellowhead Hwy 16", "dep": "09:50 AM", "arr": "11:25 AM", "km": 137.0, "mi": 85.1, "saddle": "1h 35m", "stop_dur": "35m", "activity": "Lunch + Fuel Stop", "pri_gas": "Yorkton Shell (91 V-Power)"},
            {"name": "Stage 12 Leg 3: Yorkton to Russell (Manitoba Border)", "route": "Yellowhead Hwy 16", "dep": "12:00 PM", "arr": "01:15 PM", "km": 105.0, "mi": 65.2, "saddle": "1h 15m", "stop_dur": "15m", "activity": "Manitoba Border Crossing", "pri_gas": "Russell Co-op (91 Octane)"},
            {"name": "Stage 12 Leg 4: Russell to Dauphin Escarpment", "route": "Hwy 5 & Hwy 10", "dep": "01:30 PM", "arr": "03:20 PM", "km": 129.0, "mi": 80.2, "saddle": "1h 50m", "stop_dur": "20m", "activity": "Riding Mountain Northern Escarpment Views", "pri_gas": "Dauphin Shell (91 V-Power)"}
        ],
        "arrival": "03:40 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 13, "dist_km": 440.0, "dist_mi": 273.4, "date": "Day 13 (Thu, Jul 22)",
        "title": "Dauphin to Kenora via Whiteshell", "hotel": "Clarion Lakeside Inn Kenora",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 13 Leg 1: Dauphin to Neepawa", "route": "Hwy 5 South", "dep": "07:30 AM", "arr": "08:55 AM", "km": 121.0, "mi": 75.2, "saddle": "1h 25m", "stop_dur": "20m", "activity": "Fuel + Coffee", "pri_gas": "Neepawa Esso (91 Octane)"},
            {"name": "Stage 13 Leg 2: Neepawa to Portage la Prairie", "route": "Hwy 16 East", "dep": "09:15 AM", "arr": "10:20 AM", "km": 88.0, "mi": 54.7, "saddle": "1h 05m", "stop_dur": "30m", "activity": "Early Lunch", "pri_gas": "Portage Shell (91 V-Power)"},
            {"name": "Stage 13 Leg 3: Portage to Whiteshell Granite Bluffs", "route": "Trans-Canada Hwy 1 East", "dep": "10:50 AM", "arr": "01:10 PM", "km": 145.0, "mi": 90.1, "saddle": "2h 20m", "stop_dur": "20m", "activity": "Whiteshell Park Stretch + Gas", "pri_gas": "Falcon Lake Petro-Canada"},
            {"name": "Stage 13 Leg 4: Whiteshell to Kenora / Lake of the Woods", "route": "Trans-Canada Hwy 17 East", "dep": "01:30 PM", "arr": "02:45 PM", "km": 86.0, "mi": 53.4, "saddle": "1h 15m", "stop_dur": "20m", "activity": "Welcome back to Ontario! Lakeside check-in", "pri_gas": "Kenora Shell (91 V-Power)"}
        ],
        "arrival": "03:05 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 14, "dist_km": 595.0, "dist_mi": 369.7, "date": "Day 14 (Fri, Jul 23)",
        "title": "Kenora to Nipigon Lake Superior Crossroads", "hotel": "The Red Rock Inn Historic Lodge",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 14 Leg 1: Kenora to Dryden", "route": "Hwy 17 East", "dep": "07:30 AM", "arr": "09:15 AM", "km": 142.0, "mi": 88.2, "saddle": "1h 45m", "stop_dur": "20m", "activity": "Fuel + Morning Coffee", "pri_gas": "Dryden Esso (91 Octane)"},
            {"name": "Stage 14 Leg 2: Dryden to Ignace", "route": "Hwy 17 East", "dep": "09:35 AM", "arr": "10:55 AM", "km": 106.0, "mi": 65.9, "saddle": "1h 20m", "stop_dur": "35m", "activity": "Lunch + Fuel Stop", "pri_gas": "Ignace Shell (91 V-Power)"},
            {"name": "Stage 14 Leg 3: Ignace to Thunder Bay Bypass", "route": "Hwy 17 East", "dep": "11:30 AM", "arr": "02:15 PM", "km": 211.0, "mi": 131.1, "saddle": "2h 45m", "stop_dur": "20m", "activity": "Fuel + Stretch", "pri_gas": "Thunder Bay Petro-Canada (91 Octane)"},
            {"name": "Stage 14 Leg 4: Thunder Bay to Nipigon Cable-Stayed Bridge", "route": "Hwy 17 North Shore", "dep": "02:35 PM", "arr": "04:30 PM", "km": 136.0, "mi": 84.5, "saddle": "1h 55m", "stop_dur": "25m", "activity": "Historic Red Rock Inn Waterfront Check-in", "pri_gas": "Nipigon Esso (91 Octane)"}
        ],
        "arrival": "04:55 PM", "supper": "07:00 - 08:00 PM"
    },
    {
        "day": 15, "dist_km": 400.0, "dist_mi": 248.5, "date": "Day 15 (Sat, Jul 24)",
        "title": "Nipigon to Hearst Northern Hwy 11", "hotel": "Companion Hotel Motel Hearst",
        "wake": "07:00 AM", "rollout": "07:30 AM",
        "legs": [
            {"name": "Stage 15 Leg 1: Nipigon to Beardmore Lake Nipigon Lookouts", "route": "Northern Hwy 11 North", "dep": "07:30 AM", "arr": "08:50 AM", "km": 80.0, "mi": 49.7, "saddle": "1h 20m", "stop_dur": "20m", "activity": "Lake Nipigon Vistas + World's Largest Snowman", "pri_gas": "Beardmore"},
            {"name": "Stage 15 Leg 2: Beardmore to Geraldton / Greenstone", "route": "Northern Hwy 11", "dep": "09:10 AM", "arr": "10:15 AM", "km": 89.0, "mi": 55.3, "saddle": "1h 05m", "stop_dur": "40m", "activity": "Lunch + Fuel Stop", "pri_gas": "Geraldton Esso (91 Octane)"},
            {"name": "Stage 15 Leg 3: Geraldton to Longlac Gateway", "route": "Northern Hwy 11", "dep": "10:55 AM", "arr": "11:35 AM", "km": 37.0, "mi": 23.0, "saddle": "0h 40m", "stop_dur": "20m", "activity": "MANDATORY 91 TOP-OFF + Bladder Check", "pri_gas": "Longlac Shell (91 V-Power)"},
            {"name": "Stage 15 Leg 4: Longlac to Pagwa River Wilderness to Hearst", "route": "Northern Hwy 11 Boreal", "dep": "11:55 AM", "arr": "02:45 PM", "km": 194.0, "mi": 120.5, "saddle": "2h 50m", "stop_dur": "25m", "activity": "Hearst Check-in & Cedar Sauna", "pri_gas": "Hearst Shell (91 V-Power)"}
        ],
        "arrival": "03:10 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 16, "dist_km": 260.0, "dist_mi": 161.6, "date": "Day 16 (Sun, Jul 25)",
        "title": "Hearst to Cochrane Clay Belt", "hotel": "Best Western Swan Castle Inn Cochrane",
        "wake": "07:30 AM", "rollout": "08:00 AM",
        "legs": [
            {"name": "Stage 16 Leg 1: Hearst to Kapuskasing", "route": "Northern Hwy 11 East", "dep": "08:00 AM", "arr": "09:20 AM", "km": 100.0, "mi": 62.1, "saddle": "1h 20m", "stop_dur": "30m", "activity": "Kapuskasing Riverside Park & Water Tower", "pri_gas": "Kapuskasing Esso (91 Octane)"},
            {"name": "Stage 16 Leg 2: Kapuskasing to Smooth Rock Falls", "route": "Northern Hwy 11 East", "dep": "09:50 AM", "arr": "10:55 AM", "km": 65.0, "mi": 40.4, "saddle": "1h 05m", "stop_dur": "15m", "activity": "Mattagami River Falls View", "pri_gas": "Smooth Rock Falls"},
            {"name": "Stage 16 Leg 3: Smooth Rock Falls to Cochrane", "route": "Northern Hwy 11 East", "dep": "11:10 AM", "arr": "12:30 PM", "km": 95.0, "mi": 59.0, "saddle": "1h 20m", "stop_dur": "120m", "activity": "Lunch + CANADIAN POLAR BEAR HABITAT VISIT", "pri_gas": "Cochrane Petro-Canada (91 Octane)"}
        ],
        "arrival": "02:30 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 17, "dist_km": 240.0, "dist_mi": 149.1, "date": "Day 17 (Mon, Jul 26)",
        "title": "Cochrane to Temiskaming Shores", "hotel": "Waterfront Inn New Liskeard",
        "wake": "07:30 AM", "rollout": "08:00 AM",
        "legs": [
            {"name": "Stage 17 Leg 1: Cochrane to Iroquois Falls & Matheson", "route": "Hwy 11 South", "dep": "08:00 AM", "arr": "09:30 AM", "km": 109.0, "mi": 67.7, "saddle": "1h 30m", "stop_dur": "20m", "activity": "Fuel + Morning Coffee", "pri_gas": "Matheson Esso (91 Octane)"},
            {"name": "Stage 17 Leg 2: Matheson to Kirkland Lake Junction", "route": "Hwy 11 South", "dep": "09:50 AM", "arr": "10:45 AM", "km": 56.0, "mi": 34.8, "saddle": "0h 55m", "stop_dur": "15m", "activity": "Gold Rush Crossroads", "pri_gas": "Kenogami Lake"},
            {"name": "Stage 17 Leg 3: Kirkland Lake to Earlton & Lake Timiskaming", "route": "Hwy 11 South Little Claybelt", "dep": "11:00 AM", "arr": "12:15 PM", "km": 75.0, "mi": 46.6, "saddle": "1h 15m", "stop_dur": "30m", "activity": "Earlton Giant Bison + New Liskeard Waterfront", "pri_gas": "New Liskeard Shell (91 V-Power)"}
        ],
        "arrival": "12:45 PM", "supper": "06:30 - 07:30 PM"
    },
    {
        "day": 18, "dist_km": 255.0, "dist_mi": 158.4, "date": "Day 18 (Tue, Jul 27)",
        "title": "Temiskaming Shores to Hanmer Grand Homecoming", "hotel": "Hanmer Home Base (0.0 m Loop Closure!)",
        "wake": "07:30 AM", "rollout": "08:15 AM",
        "legs": [
            {"name": "Stage 18 Leg 1: New Liskeard to Temagami Old Growth Pines", "route": "Hwy 11 South", "dep": "08:15 AM", "arr": "09:30 AM", "km": 72.0, "mi": 44.7, "saddle": "1h 15m", "stop_dur": "35m", "activity": "Temagami Fire Tower on Caribou Mountain", "pri_gas": "Temagami Shell (91 V-Power)"},
            {"name": "Stage 18 Leg 2: Temagami to North Bay Waterfront", "route": "Hwy 11 South", "dep": "10:05 AM", "arr": "11:35 AM", "km": 92.0, "mi": 57.2, "saddle": "1h 30m", "stop_dur": "45m", "activity": "Lunch on Lake Nipissing Waterfront", "pri_gas": "North Bay Esso (91 Octane)"},
            {"name": "Stage 18 Leg 3: North Bay to Sturgeon Falls & Hanmer Home Base", "route": "Hwy 17 West to Hanmer", "dep": "12:20 PM", "arr": "02:00 PM", "km": 91.0, "mi": 56.5, "saddle": "1h 40m", "stop_dur": "0m", "activity": "GRAND EXPEDITION HOMECOMING! 0.0 m LOOP CLOSURE", "pri_gas": "Hanmer"}
        ],
        "arrival": "02:00 PM", "supper": "06:00 - 08:00 PM (Celebratory Dinner)"
    }
]

print("Generating 18-day Gantt chart component...")
gantt_html = generate_gantt_html(
    days_data,
    title="Heart of the Rockies &amp; Mount Robson Master Saddle Timeline",
    subtitle="Visualizing daily rhythms • <strong>07:00 AM standard starts</strong> • <strong>30m breakfast &amp; lunch</strong> • <strong>1h supper</strong> • <strong>≤110–135 mi fuel pacing</strong> • <strong>0.0 m loop closure</strong>",
    base_hour=6,
    end_hour=24
)

index_path = r"C:\Users\Jamie\Desktop\Rockies and Mount Robson Expedition\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update title and navigation downloads
downloads_html = """
            <div id="sec-downloads" class="downloads-section" style="margin-top: 32px; padding: 20px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; box-shadow: var(--card-shadow);">
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
                    <span>📥</span> Expedition Navigation Assets &amp; Field Guides
                </div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                    1-tap offline navigation packages for GPS units, smartphones, and field briefing.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                    <a href="rockies_tracks.gpx" download class="btn-download" style="display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 700; font-size: 0.88rem;">
                        <span style="font-size: 1.3rem;">🧭</span>
                        <div>
                            <div>Garmin GPX 1.1</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">18 Tracks • 92 Waypoints</div>
                        </div>
                    </a>
                    <a href="rockies_tracks.kml" download class="btn-download" style="display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 700; font-size: 0.88rem;">
                        <span style="font-size: 1.3rem;">🌍</span>
                        <div>
                            <div>Google Earth KML</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">3D Elevation Polylines</div>
                        </div>
                    </a>
                    <a href="rockies_pois.csv" download class="btn-download" style="display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 700; font-size: 0.88rem;">
                        <span style="font-size: 1.3rem;">📍</span>
                        <div>
                            <div>Curated POIs CSV</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">Rates, Phones, 91 AKI</div>
                        </div>
                    </a>
                    <a href="rockies_saddle_logistics.md" download class="btn-download" style="display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 700; font-size: 0.88rem;">
                        <span style="font-size: 1.3rem;">📋</span>
                        <div>
                            <div>Saddle &amp; Fuel Dossier</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">Timing &amp; Booster Protocol</div>
                        </div>
                    </a>
                    <a href="rockies_secret_gems.md" download class="btn-download" style="display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text-main); font-weight: 700; font-size: 0.88rem;">
                        <span style="font-size: 1.3rem;">💎</span>
                        <div>
                            <div>Secret Gems Guide</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">Mt Robson &amp; Icefields Vistas</div>
                        </div>
                    </a>
                </div>
            </div>
"""

# Replace downloads section with enriched downloads
content = re.sub(r'<div id="sec-downloads"[^>]*>.*?</div>\s*</div>\s*</div>', f'{gantt_html}\n{downloads_html}</div></div>', content, flags=re.DOTALL)

# 2. Update Mobile Bottom Nav to 5 tabs: Map, Itinerary, Timeline, Downloads, Notes
new_bottom_nav = """
    <!-- Mobile Fixed Bottom Navigation Bar (5 Dedicated Tabs) -->
    <nav id="mobile-bottom-nav">
        <button class="mobile-nav-btn active" id="btn-tab-map" onclick="switchMobileTab('map')">
            <span class="nav-icon">🗺️</span>
            <span class="nav-label">Map</span>
        </button>
        <button class="mobile-nav-btn" id="btn-tab-feed" onclick="switchMobileTab('feed')">
            <span class="nav-icon">📋</span>
            <span class="nav-label">Itinerary</span>
        </button>
        <button class="mobile-nav-btn" id="btn-tab-timeline" onclick="switchMobileTab('timeline')">
            <span class="nav-icon">⏱️</span>
            <span class="nav-label">Timeline</span>
        </button>
        <button class="mobile-nav-btn" id="btn-tab-downloads" onclick="switchMobileTab('downloads')">
            <span class="nav-icon">📥</span>
            <span class="nav-label">Files</span>
        </button>
        <button class="mobile-nav-btn" id="btn-tab-notes" onclick="openTripNotesModal()">
            <span class="nav-icon">💬</span>
            <span class="nav-label">Notes</span>
        </button>
    </nav>
"""
content = re.sub(r'<nav id="mobile-bottom-nav">.*?</nav>', new_bottom_nav.strip(), content, flags=re.DOTALL)

# 3. Add Notes button in Header Controls
notes_header_btn = """
            <button type="button" class="btn-trip-notes" id="btn-header-notes" onclick="openTripNotesModal()" title="Expedition Notes & AI Fine-Tuning Studio" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-weight: 700; font-size: 0.8rem; cursor: pointer; transition: all 0.2s ease;">
                <span>💬</span>
                <span>Notes</span>
                <span class="notes-badge-count" id="header-notes-badge" style="background: var(--accent-blue); color: #fff; padding: 2px 6px; border-radius: 10px; font-size: 0.7rem; display: none;">0</span>
            </button>
"""
if 'btn-header-notes' not in content:
    content = content.replace('<div class="split-presets">', f'{notes_header_btn}\n            <div class="split-presets">')

# 4. Inject Action Buttons (Zoom Map, Google Maps Directions, + Note) on each Day Card
for day_num in range(1, 19):
    old_btn = f'<button class="btn-zoom" onclick="event.stopPropagation(); focusDay({day_num})">🎯 Zoom Map to Day {day_num} Track</button>'
    new_btn = f'''<div class="day-actions-row" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;">
                        <button type="button" class="btn-action-zoom" onclick="event.stopPropagation(); focusDay({day_num})" style="flex: 1; min-width: 130px; padding: 8px 12px; background: var(--accent-blue); color: #ffffff; border: none; border-radius: 6px; font-weight: 700; font-size: 0.8rem; cursor: pointer;">🎯 Zoom Map</button>
                        <button type="button" class="btn-day-note" onclick="event.stopPropagation(); openTripNotesModal({{day: {day_num}, title: 'Day {day_num}'}});" style="padding: 8px 14px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-weight: 700; font-size: 0.8rem; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                            <span>💬</span> Note
                        </button>
                    </div>'''
    content = content.replace(old_btn, new_btn)

# 5. In-App Trip Notes Modal HTML
trip_notes_modal_html = """
    <!-- In-App Trip Notes & AI Fine-Tuning Studio Modal -->
    <div id="trip-notes-modal" style="display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(4px); z-index: 9999; justify-content: center; align-items: center; padding: 16px;">
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; max-width: 640px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
            <!-- Modal Header -->
            <div style="padding: 16px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface);">
                <div>
                    <h3 style="margin: 0; font-size: 1.15rem; color: var(--text-main); display: flex; align-items: center; gap: 8px;">
                        <span>💬</span> Expedition Notes &amp; AI Fine-Tuning Studio
                    </h3>
                    <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 3px;">
                        Add reminders, road notes, or adjustment requests. Generates 1-click prompts for Antigravity AI!
                    </div>
                </div>
                <button type="button" onclick="closeTripNotesModal()" style="background: none; border: none; font-size: 1.4rem; color: var(--text-muted); cursor: pointer; padding: 4px;">&times;</button>
            </div>

            <!-- Modal Body -->
            <div style="padding: 16px 20px; overflow-y: auto; flex: 1;">
                <!-- Add Note Form -->
                <div style="background: var(--bg-base); border: 1px solid var(--border); border-radius: 10px; padding: 14px; margin-bottom: 16px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-main); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">Add New Route Note or Adjustment</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
                        <select id="note-target-day" style="padding: 8px 10px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-size: 0.8rem;">
                            <option value="0">General Expedition Note</option>
                            <option value="1">Day 1: Hanmer to Wawa</option>
                            <option value="2">Day 2: Wawa to Thunder Bay</option>
                            <option value="3">Day 3: Thunder Bay to Kenora</option>
                            <option value="4">Day 4: Kenora to Regina</option>
                            <option value="5">Day 5: Regina to Medicine Hat</option>
                            <option value="6">Day 6: Medicine Hat to Canmore/Banff</option>
                            <option value="7">Day 7: Banff & Yoho NP Loop</option>
                            <option value="8">Day 8: Icefields Parkway to Jasper</option>
                            <option value="9">Day 9: Mount Robson (BC) Excursion</option>
                            <option value="10">Day 10: Jasper to Edmonton</option>
                            <option value="11">Day 11: Edmonton to Saskatoon</option>
                            <option value="12">Day 12: Saskatoon to Dauphin</option>
                            <option value="13">Day 13: Dauphin to Kenora</option>
                            <option value="14">Day 14: Kenora to Nipigon</option>
                            <option value="15">Day 15: Nipigon to Hearst (Hwy 11)</option>
                            <option value="16">Day 16: Hearst to Cochrane</option>
                            <option value="17">Day 17: Cochrane to Temiskaming Shores</option>
                            <option value="18">Day 18: Temiskaming Shores to Hanmer</option>
                        </select>
                        <select id="note-category" style="padding: 8px 10px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-size: 0.8rem;">
                            <option value="Route ⚠️">Route / Detour ⚠️</option>
                            <option value="Fuel ⛽">Fuel / 91 Octane ⛽</option>
                            <option value="Hotel 🏨">Hotel / Cabins 🏨</option>
                            <option value="Sight ⭐">Scenic Gem / Hike ⭐</option>
                            <option value="Food 🍽️">Dining / Coffee 🍽️</option>
                        </select>
                    </div>
                    <textarea id="note-text-input" rows="3" placeholder="Enter note, scenic detour request, or preference (e.g., 'Add stop at Athabasca Falls parking lot' or 'Check if 91 octane is reliable in Longlac')..." style="width: 100%; box-sizing: border-box; padding: 10px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-size: 0.82rem; font-family: inherit; resize: vertical; margin-bottom: 10px;"></textarea>
                    <div style="display: flex; justify-content: flex-end; gap: 8px;">
                        <button type="button" onclick="saveTripNote()" style="padding: 8px 16px; background: var(--accent-blue); color: #fff; border: none; border-radius: 6px; font-weight: 700; font-size: 0.8rem; cursor: pointer;">Save Note</button>
                    </div>
                </div>

                <!-- Notes List & AI Actions -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
                        Saved Notes (<span id="notes-total-count">0</span>)
                    </div>
                    <div style="display: flex; gap: 6px;">
                        <button type="button" onclick="copyTripNotesPrompt()" style="padding: 6px 12px; background: #10b981; color: #fff; border: none; border-radius: 6px; font-weight: 700; font-size: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                            <span>📋</span> Copy Prompt for AI
                        </button>
                        <button type="button" onclick="exportTripNotesMarkdown()" style="padding: 6px 10px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-weight: 600; font-size: 0.75rem; cursor: pointer;">
                            📥 Export .md
                        </button>
                        <button type="button" onclick="clearAllTripNotes()" style="padding: 6px 10px; background: var(--bg-base); border: 1px solid var(--border); border-radius: 6px; color: var(--accent-red); font-weight: 600; font-size: 0.75rem; cursor: pointer;">
                            🗑️ Clear
                        </button>
                    </div>
                </div>
                <div id="notes-list-container"></div>
            </div>
        </div>
    </div>
"""

# Append Trip Notes modal before </body>
content = content.replace('</body>', f'{trip_notes_modal_html}\n</body>')

# 6. Add JavaScript functions for Notes & Tab switching
js_notes_code = """
        // --- In-App Trip Notes & AI Fine-Tuning Studio Logic ---
        const NOTES_STORAGE_KEY = 'rockies_mount_robson_trip_notes_v1';

        function loadTripNotes() {
            try {
                const raw = localStorage.getItem(NOTES_STORAGE_KEY);
                return raw ? JSON.parse(raw) : [];
            } catch (e) {
                return [];
            }
        }

        function saveTripNotesToStorage(notes) {
            try {
                localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(notes));
            } catch (e) {}
            updateNotesBadges();
        }

        function updateNotesBadges() {
            const notes = loadTripNotes();
            const count = notes.length;
            const headerBadge = document.getElementById('header-notes-badge');
            if (headerBadge) {
                headerBadge.textContent = count;
                headerBadge.style.display = count > 0 ? 'inline-block' : 'none';
            }
            const totalCount = document.getElementById('notes-total-count');
            if (totalCount) totalCount.textContent = count;
        }

        function openTripNotesModal(preset) {
            const modal = document.getElementById('trip-notes-modal');
            if (!modal) return;
            if (preset && typeof preset.day !== 'undefined') {
                const sel = document.getElementById('note-target-day');
                if (sel) sel.value = preset.day;
            }
            modal.style.display = 'flex';
            renderTripNotesList();
            updateNotesBadges();
            setTimeout(() => {
                const txt = document.getElementById('note-text-input');
                if (txt) txt.focus();
            }, 100);
        }

        function closeTripNotesModal() {
            const modal = document.getElementById('trip-notes-modal');
            if (modal) modal.style.display = 'none';
        }

        function saveTripNote() {
            const txtEl = document.getElementById('note-text-input');
            const targetEl = document.getElementById('note-target-day');
            const catEl = document.getElementById('note-category');
            if (!txtEl || !txtEl.value.trim()) return;

            const dayNum = parseInt(targetEl ? targetEl.value : '0', 10);
            const targetText = targetEl && targetEl.selectedOptions ? targetEl.selectedOptions[0].text : 'General Note';
            const category = catEl ? catEl.value : 'Route ⚠️';
            const text = txtEl.value.trim();

            const notes = loadTripNotes();
            notes.unshift({
                id: 'note_' + Date.now(),
                day: dayNum,
                target: targetText,
                category: category,
                text: text,
                dateStr: new Date().toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
            });

            saveTripNotesToStorage(notes);
            txtEl.value = '';
            renderTripNotesList();
        }

        function deleteTripNote(id) {
            let notes = loadTripNotes();
            notes = notes.filter(n => n.id !== id);
            saveTripNotesToStorage(notes);
            renderTripNotesList();
        }

        function clearAllTripNotes() {
            if (confirm('Clear all expedition notes?')) {
                saveTripNotesToStorage([]);
                renderTripNotesList();
            }
        }

        function renderTripNotesList() {
            const container = document.getElementById('notes-list-container');
            if (!container) return;
            const notes = loadTripNotes();

            if (notes.length === 0) {
                container.innerHTML = `
                    <div style="background: var(--bg-base); border: 1px dashed var(--border); border-radius: 8px; padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
                        No notes recorded yet. Add an adjustment or reminder above!
                    </div>`;
                return;
            }

            let html = '';
            notes.forEach(n => {
                html += `
                    <div style="background: var(--bg-base); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="background: var(--bg-card); border: 1px solid var(--border); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.72rem; color: var(--accent-blue);">${n.target}</span>
                                <span style="font-size: 0.75rem; color: var(--text-muted);">${n.category}</span>
                            </div>
                            <button type="button" onclick="deleteTripNote('${n.id}')" style="background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 0.8rem;">&times;</button>
                        </div>
                        <div style="font-size: 0.82rem; color: var(--text-main); line-height: 1.4;">${n.text}</div>
                        <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 6px; text-align: right;">${n.dateStr}</div>
                    </div>`;
            });
            container.innerHTML = html;
        }

        function copyTripNotesPrompt() {
            const notes = loadTripNotes();
            if (notes.length === 0) {
                alert('No notes to copy. Please add a note first.');
                return;
            }
            let prompt = '# Feedback & Route Fine-Tuning Instructions for Antigravity AI\\n\\n';
            prompt += 'Please update the Heart of the Rockies & Mount Robson 18-Day Expedition itinerary according to my field notes:\\n\\n';
            notes.forEach(n => {
                prompt += `- **[${n.target}]** (${n.category}): ${n.text}\\n`;
            });
            navigator.clipboard.writeText(prompt).then(() => {
                alert('📋 Copied AI Fine-Tuning Prompt to clipboard! Paste it directly into Antigravity.');
            });
        }

        function exportTripNotesMarkdown() {
            const notes = loadTripNotes();
            if (notes.length === 0) {
                alert('No notes to export.');
                return;
            }
            let md = '# Expedition Notes: Rockies & Mount Robson\\n\\n';
            notes.forEach(n => {
                md += `### ${n.target} - ${n.category}\\n*Recorded: ${n.dateStr}*\\n\\n${n.text}\\n\\n---\\n\\n`;
            });
            const blob = new Blob([md], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'rockies_mount_robson_notes.md';
            a.click();
            URL.revokeObjectURL(url);
        }

        // Initialize notes badges on page load
        document.addEventListener('DOMContentLoaded', () => {
            updateNotesBadges();
        });
"""

content = content.replace('// --- Helper: Get CSS variable value ---', f'{js_notes_code}\n        // --- Helper: Get CSS variable value ---')

# 7. Add mobile tab rules for tab-timeline and tab-downloads in switchMobileTab
switch_tab_code = """
        function switchMobileTab(tab) {
            document.body.classList.remove('tab-map', 'tab-feed', 'tab-timeline', 'tab-downloads');
            document.body.classList.add('tab-' + tab);

            document.querySelectorAll('#mobile-bottom-nav .mobile-nav-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            const activeBtn = document.getElementById('btn-tab-' + tab);
            if (activeBtn) activeBtn.classList.add('active');

            if (tab === 'map') {
                setTimeout(() => {
                    if (map) map.invalidateSize();
                }, 50);
            } else if (tab === 'timeline') {
                const el = document.getElementById('sec-gantt');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            } else if (tab === 'downloads') {
                const el = document.getElementById('sec-downloads');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
            }
        }
"""
content = re.sub(r'function switchMobileTab\(tab\)\s*\{.*?\}', switch_tab_code.strip(), content, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully enriched {index_path} with Gantt chart, Notes studio, and mobile tabs!")
