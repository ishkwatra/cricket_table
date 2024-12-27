document.addEventListener("DOMContentLoaded", () => {
    const standingsBody = document.getElementById("standings-body");
    const matchesList = document.getElementById("matches-list");
    const updateButton = document.getElementById("update-button");

    let data = null;

    // Fetch initial data
    fetch("/")
        .then(response => response.json())
        .then(initData => {
            data = initData;
            renderStandings(data.teams);
            renderMatches(data.remaining_matches);
        });

    // Render standings
    function renderStandings(teams) {
        standingsBody.innerHTML = "";
        teams.forEach((team, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${team.name}</td>
                <td>${team.matches}</td>
                <td>${team.wins}</td>
                <td>${team.losses}</td>
                <td>${team.points}</td>
                <td>${team.pct}%</td>
            `;
            standingsBody.appendChild(row);
        });
    }

    // Render matches
    function renderMatches(matches) {
        matchesList.innerHTML = "";
        matches.forEach((match, index) => {
            const matchItem = document.createElement("div");
            matchItem.classList.add("match-item");
            matchItem.innerHTML = `
                <span>${match.team1} vs ${match.team2}</span>
                <select data-index="${index}" class="match-outcome">
                    <option value="none">Select Outcome</option>
                    <option value="team1">${match.team1} Wins</option>
                    <option value="team2">${match.team2} Wins</option>
                    <option value="draw">Draw</option>
                </select>
            `;
            matchesList.appendChild(matchItem);
        });
    }

    // Update standings on button click
    updateButton.addEventListener("click", () => {
        const outcomes = Array.from(document.querySelectorAll(".match-outcome")).map(select => select.value);

        if (outcomes.includes("none")) {
            alert("Please select outcomes for all matches.");
            return;
        }

        fetch("/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ outcomes })
        })
            .then(response => response.json())
            .then(updatedData => {
                renderStandings(updatedData.teams);
            })
            .catch(error => console.error("Error updating standings:", error));
    });
});
