async function get_list() {
    try {
        const response = await fetch(statUrl, {
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

function add_item(item) {
    let dynamic_stats = document.getElementById("dynamic_stats");

    // Creates an object element
    let new_item = document.createElement("div");
    new_item.innerHTML = item;
    dynamic_stats.appendChild(new_item);
}

// Using async/await to handle the asynchronous data
async function initialize() {
    try {
        const data = await get_list();
        if (data && data.length) {
            for (let i = 0; i < data.length; i++) {
                add_item(data[i]);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call the initialize function when the script loads
// noinspection JSIgnoredPromiseFromCall
initialize();