async function get_list(server_url) {
    try {
        const response = await fetch(`${server_url}/api/list_statistics`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            // noinspection ExceptionCaughtLocallyJS
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
}

function add_item(name, statData, server_url) {
    let dynamic_stats = document.getElementById("dynamic_stats");

    // Create the HTML template for the new item
    let href_url = `${server_url}/view/${name}`;
    // noinspection JSUnresolvedReference
    const itemHTML = `
        <a class="stat-item" href=${href_url}>
            <div class="stat-header">
                <h3 class="stat-title">${name}</h3>
                <span class="stat-type">${statData.type}</span>
            </div>
            <p class="stat-description">${statData.description}</p>
            <div class="stat-footer">
                <span class="trend-status">${statData.trend_analysis.enabled ? 'Trend Analysis Enabled' : 'No Trend Analysis'}</span>
            </div>
        </a>
    `;

    // Create a new div element and set its innerHTML
    let new_item = document.createElement("div");
    new_item.innerHTML = itemHTML;
    
    // Append the new item to the dynamic stats container
    dynamic_stats.appendChild(new_item);
}

async function initialize_list(server_url) {
    try {
        const data = await get_list(server_url);
        console.log('Received data:', data); // Debug log
        
        if (data) {
            // Iterate over the object's key-value pairs
            for (const [statName, statData] of Object.entries(data)) {
                add_item(statName, statData, server_url);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}