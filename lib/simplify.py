def time(wdTime):
    assert wdTime["type"] == "time"
    wdValue    = wdTime["value"]
    simpleTime = {"type": "time", "value":  wdValue["time"][1:] if wdValue["time"].startswith("+") else wdValue["time"]}

    for property in ("after", "before", "timezone"):
        if  wdValue[property] != 0:
            simpleTime[property] =  wdValue[property]

    if wdValue["calendarmodel"] != "http://www.wikidata.org/entity/Q1985727":
        simpleTime["calendarmodel"] =  wdValue["calendarmodel"]

    # If precision is a day or less, it's just a date
    if  wdValue["precision"] <= 11:
        simpleTime["type"]  = "date"
        simpleTime["value"] =  simpleTime["value"][:simpleTime["value"].find("T")]

        # Accurate to less than a day
        if wdValue["precision"] < 11:
            simpleTime["precision"] = wdValue["precision"]

    # More accurate than a day but less that a second
    elif wdValue["precision"] < 14:
        simpleTime["precision"] = wdValue["precision"]

    return simpleTime
