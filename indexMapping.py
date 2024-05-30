indexMapping = {
    "properties": {
        "MatchID": {
            "type": "long"
        },
        "Time (Brazil)": {
            "type": "text"
        },
        "Date": {
            "type": "text"
        },
        "Stage": {
            "type": "text"
        },
        "Stadium": {
            "type": "text"
        },
        "City": {
            "type": "text"
        },
        "Home Team": {
            "type": "text"
        },
        "Home Team Goals": {
            "type": "long"
        },
        "Away Team Goals": {
            "type": "long"
        },
        "Away Team": {
            "type": "text"
        },
        "Win Conditions": {
            "type": "text"
        },
        "Penalty": {
            "type": "text"
        },
        "Win": {
            "type": "text"
        },
        "Total Goals": {
            "type": "long"
        },
        "Attendance": {
            "type": "long"
        },
        "CityVector":{
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "l2_norm"
        }
        
    }
}