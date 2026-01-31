// Enable tab key in code textareas in Django admin
document.addEventListener('DOMContentLoaded', function() {
    // Target the code, stdout, and stderr textareas
    const textareas = document.querySelectorAll('textarea[name="code"], textarea[name="stdout"], textarea[name="stderr"]');
    
    textareas.forEach(function(textarea) {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                const value = this.value;
                // Insert 4 spaces (Python standard)
                this.value = value.substring(0, start) + '    ' + value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    });
});
