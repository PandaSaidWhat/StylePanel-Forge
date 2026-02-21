// extensions/StylePanel/javascript/ucp_weighting.js
// Global listener for CTRL + ArrowUp/Down weighting in the UCP preview box
onUiLoaded(() => {
    console.log("[UCP] Pro-weighting listener active.");
    
    document.addEventListener('keydown', (e) => {
        // Trigger on CTRL + ArrowUp or ArrowDown
        if (e.ctrlKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
            const target = e.target;
            
            // Only execute if the focus is inside the positive preview textarea
            if (target.tagName === 'TEXTAREA' && target.closest('#ucp_positive_preview')) {
                e.preventDefault();
                
                let start = target.selectionStart;
                let end = target.selectionEnd;
                let text = target.value;
                let selected = text.substring(start, end);

                if (!selected) return;

                let step = e.key === 'ArrowUp' ? 0.1 : -0.1;
                
                // Regex to capture existing weighting (word:weight) - supports negative numbers and decimals
                let match = selected.match(/^\((.*):(-?\d+\.?\d*)\)$/);
                let newText;

                if (match) {
                    // Rounding to one decimal place to avoid floating point errors
                    let currentVal = parseFloat(match[2]);
                    let newVal = Math.round((currentVal + step) * 10) / 10;
                    
                    // Remove weighting completely if it reaches 1.0 (Standard Forge behavior)
                    if (newVal === 1.0) {
                        newText = match[1];
                    } else {
                        newText = `(${match[1]}:${newVal.toFixed(1)})`;
                    }
                } else {
                    // If the word has no weighting, start at 1.1 or 0.9
                    let newVal = Math.round((1.0 + step) * 10) / 10;
                    // Skip 1.0 as it equals no parenthesis
                    newText = `(${selected}:${newVal.toFixed(1)})`;
                }

                // Update the textarea value and maintain the selection
                target.value = text.substring(0, start) + newText + text.substring(end);
                target.selectionStart = start;
                target.selectionEnd = start + newText.length;
                
                // Notify Gradio that the input has changed
                target.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }, true);
});