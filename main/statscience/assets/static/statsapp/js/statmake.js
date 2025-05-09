document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('stat_form');
    const toast = document.getElementById('toast');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from being submitted traditionally

        const formData = new FormData(form);  // Gather all form data

        // noinspection JSUnusedLocalSymbols
        fetch(statUrl, {  // Use the injected variable for the URL
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

    function showToast(message) {
        toast.innerText = message;
        toast.style.display = "block";  // Show toast
        setTimeout(() => { toast.style.display = "none"; }, 4000);  // Hide toast after 4 seconds
    }
});
