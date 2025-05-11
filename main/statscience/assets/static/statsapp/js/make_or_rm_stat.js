
function initializeStatForm(mode, form_id) {
    const form = document.getElementById(form_id);
    const toast = document.getElementById('toast');

    function showToast(message) {
        toast.innerText = message;
        toast.style.display = "block";  // Show toast
        setTimeout(() => { toast.style.display = "none"; }, 4000);  // Hide toast after 4 seconds
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from being submitted traditionally

        const formData = new FormData(form);  // Gather all form data

        // noinspection JSUnusedAssignment
        let statUrl = null;
        if (mode === 'create') {
            statUrl = `${window.location.origin}/api/statistic_create`;
        }
        else {
            statUrl = `${window.location.origin}/api/statistic_delete`;
        }
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
}