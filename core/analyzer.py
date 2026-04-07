from collections import defaultdict

def classify(subs):
    data = defaultdict(list)

    for s in subs:
        if any(x in s for x in ["admin", "dev", "staging"]):
            data["high"].append(s)
        elif "api" in s:
            data["medium"].append(s)
        else:
            data["low"].append(s)

    return data