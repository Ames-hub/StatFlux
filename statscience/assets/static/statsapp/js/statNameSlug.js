function slugify(text) {
    return text
        .toString()
        .normalize('NFKD')
        .replace(/[\u0300-\u036F]/g, '')
        .replace(/[^\w\-]+/g, '-')
        .replace(/--+/g, '-')
        .replace(/^-+/, '')
        .replace(/-+$/, '')
}

function initializeSlugWatcher() {
    const nameInput = document.querySelector('input[name="stat_name"]');
    const output = document.getElementById('slug_output');
    const wrapper = output?.parentElement;

    if (nameInput && output && wrapper) {
        nameInput.addEventListener('input', () => {
            const raw = nameInput.value;
            const slug = slugify(raw);

            // Only show the slug output if it's different from raw input
            if (slug !== raw) {
                output.textContent = slug || '...';
                wrapper.style.display = 'block';
            } else {
                wrapper.style.display = 'none';
            }
        });

        // Triggers once it loads
        const raw = nameInput.value;
        const slug = slugify(raw);
        if (slug !== raw) {
            output.textContent = slug || '...';
            wrapper.style.display = 'block';
        } else {
            wrapper.style.display = 'none';
        }
    }
}
