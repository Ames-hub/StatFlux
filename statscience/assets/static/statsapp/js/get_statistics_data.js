function get_data(stat_name) {
    // uses FETCH to get from the django API
    return fetch(`${window.location.origin}/api/get_stat_data/${stat_name}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('Error fetching statistics data:', error);
            throw error;
        });
}