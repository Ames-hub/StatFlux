function InitDataSubmitForm(submission_url, stat_name) {
    const form = document.getElementById('data_submit_form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from being submitted traditionally

        const formData = new FormData(form);  // Gather all form data
        formData.append('stat_name', stat_name);

        const toast = document.getElementById('toast');
        function showToast(message) {
            toast.innerText = message;
            toast.style.display = "block";  // Show toast
            setTimeout(() => { toast.style.display = "none"; }, 4000);  // Hide toast after 4 seconds
        }

        // noinspection JSUnusedLocalSymbols
        fetch(`${submission_url}`, {  // Use the injected variable for the URL
            method: "POST",
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value  // Include CSRF token
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message);
                    (async function() {
                        await create_graph(stat_name);
                    })();
                    form.reset();  // Optionally reset the form
                } else {
                    let errorText = Object.entries(data.errors).map(([k, v]) => `${k}: ${v.join(', ')}`).join('\n');
                    showToast("Error:\n" + errorText);
                }
            })
            .catch(err => {
                showToast("Something went wrong. Please try again.");
            });
    });
}