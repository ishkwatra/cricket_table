from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


# Current standings data
table_org = [
    {"name": "South Africa", "matches": 11, "wins": 7,
        "losses": 3, "tie": 1, "ded": 0, "points": 0, "pct": 0},
    {"name": "Australia", "matches": 16, "wins": 10, "losses": 4,
        "tie": 2, "ded": 10, "points": 0, "pct": 0},
    {"name": "India", "matches": 18, "wins": 9, "losses": 7,
        "tie": 2, "ded": 2, "points": 0, "pct": 0},
    {"name": "New Zealand", "matches": 14, "wins": 7,
        "losses": 7, "tie": 0, "ded": 3, "points": 0, "pct": 0},
    {"name": "Sri Lanka", "matches": 11, "wins": 5,
        "losses": 6, "tie": 0, "ded": 0, "points": 0, "pct": 0},
    {"name": "England", "matches": 22, "wins": 11, "losses": 10,
        "tie": 1, "ded": 22, "points": 0, "pct": 0},
    {"name": "Bangladesh", "matches": 12, "wins": 4,
        "losses": 8, "tie": 0, "ded": 3, "points": 0, "pct": 0},
    {"name": "Pakistan", "matches": 11, "wins": 4, "losses": 7,
        "tie": 0, "ded": 8, "points": 0, "pct": 0},
    {"name": "West Indies", "matches": 11, "wins": 2,
        "losses": 7, "tie": 2, "ded": 0, "points": 0, "pct": 0}
]
for team in table_org:
    matches = team['matches']
    team['points'] = team['wins']*12+team['tie']*4-team['ded']
    team['pct'] = round((team['points'] / (matches * 12))
                        * 100, 2) if matches > 0 else 0
table = [
    table_org[0].copy(),
    table_org[1].copy(),
    table_org[2].copy(),
    table_org[3].copy(),
    table_org[4].copy(),
    table_org[5].copy(),
    table_org[6].copy(),
    table_org[7].copy(),
    table_org[8].copy(),
]
remaining_matches = [

    {"team1": "Australia", "team2": "India"},
    {"team1": "Australia", "team2": "Sri Lanka"},
    {"team1": "Australia", "team2": "Sri Lanka"},
    {"team1": "Pakistan", "team2": "South Africa"},
    {"team1": "Pakistan", "team2": "West Indies"},
    {"team1": "Pakistan", "team2": "West Indies"},
]


@ app.route('/')
def index():
    return render_template('index.html')


@app.route("/data", methods=["GET"])
def get_data():
    return jsonify({"teams": table, "remaining_matches": remaining_matches})


@ app.route('/update', methods=['POST'])
def update_table():
    outcomes = request.json.get('outcomes', [])

    # Simulate match results and calculate updated standings
    updated_data = simulate_outcomes(table, remaining_matches, outcomes)

    return jsonify(updated_data)


def simulate_outcomes(table, remaining_matches, outcomes):
    table = [
        table_org[0].copy(),
        table_org[1].copy(),
        table_org[2].copy(),
        table_org[3].copy(),
        table_org[4].copy(),
        table_org[5].copy(),
        table_org[6].copy(),
        table_org[7].copy(),
        table_org[8].copy(),
    ]

    for i, outcome in enumerate(outcomes):
        if outcome == "none":
            continue
        team1 = remaining_matches[i]['team1']
        team11 = 0
        for x in table:
            if x['name'] == team1:
                break
            else:
                team11 += 1
        team2 = remaining_matches[i]['team2']
        team22 = 0
        for x in table:
            if x['name'] == team2:
                break
            else:
                team22 += 1
        if outcome == 'team1':
            table[team11]['wins'] += 1
            table[team22]['losses'] += 1
        elif outcome == 'team2':
            table[team22]['wins'] += 1
            table[team11]['losses'] += 1
        elif outcome == 'draw':
            table[team11]['tie'] += 1
            table[team22]['tie'] += 1

        # Update matches played
        table[team11]['matches'] += 1
        table[team22]['matches'] += 1

    # Calculate percentages
    for team in table:
        matches = team['matches']
        team['points'] = team['wins']*12+team['tie']*4-team['ded']
        team['pct'] = round((team['points'] / (matches * 12))
                            * 100, 2) if matches > 0 else 0

    # Return sorted standings
    sorted_teams = sorted(table, key=lambda x: x['pct'], reverse=True)
    return {"teams": sorted_teams}


'''
# temp
@ app.route('/temp', methods=['POST'])
def temp():
    team11 = 0
    for x in table_org:
        if x['name'] == "India":
            break
        else:
            team11 += 1
    table_org[team11]['ded'] += 0

    # Calculate percentages
    for team in table_org:
        matches = team['matches']
        team['points'] = team['wins']*12+team['tie']*4-team['ded']
        team['pct'] = round((team['points'] / (matches * 12))
                            * 100, 2) if matches > 0 else 0
    # sort again
    sorted_teams = sorted(table_org, key=lambda x: x['pct'], reverse=True)
    updated = {"teams": sorted_teams}
    return jsonify(updated)
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
