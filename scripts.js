document.addEventListener('DOMContentLoaded', () => {
    updateStandings();

    // Toggle between night and light modes
    document.getElementById('toggle-mode-button').addEventListener('click', () => {
        document.body.classList.toggle('night-mode');
        document.body.classList.toggle('light-mode');
    });
});

document.getElementById('update-button').addEventListener('click', updateStandings);

async function updateStandings() {
    try {
        const response = await fetch('http://127.0.0.1:5000/update-standings');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const tbody = document.querySelector('#drivers-table tbody');
        tbody.innerHTML = '';

        data.forEach(driver => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cleanData(driver.rank)}</td>
                <td><img src="${driver.flag_url}" alt="Flag" style="width: 16px; height: 12px;"> ${cleanData(driver.driver)}</td>
                <td>${cleanData(driver.team)}</td>
                <td>${cleanData(driver.wins)}</td>
                <td>${cleanData(driver.points)}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching the standings:', error);
    }
}

function cleanData(data) {
    // Remove any duplicate numbers or unwanted characters
    return data.replace(/(\d+)\1+/, '$1');
}
