import sys

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openPdfModal
old_open = '''            document.body.style.overflow = 'auto'; // Lascia fare lo scroll nativo al body
            document.body.style.overscrollBehaviorY = 'none'; // Previene il pull-to-refresh'''

new_open = '''            document.body.style.overflow = 'auto';
            document.documentElement.style.overscrollBehaviorY = 'none';
            document.body.style.overscrollBehaviorY = 'none';'''

content = content.replace(old_open, new_open)

# 2. Update closePdfModal
old_close = '''            modal.classList.remove('block', 'min-h-screen', 'bg-white');
            document.body.style.overscrollBehaviorY = '';'''

new_close = '''            modal.classList.remove('block', 'min-h-screen', 'bg-white');
            document.documentElement.style.overscrollBehaviorY = '';
            document.body.style.overscrollBehaviorY = '';'''

content = content.replace(old_close, new_close)

# 3. Update swipe logic to use isPinching
old_swipe = '''        let touchstartX = 0;
        let touchendX = 0;
        function handlePdfSwipe() {
            if (currentPlaylist.length <= 1) return;
            // Se l'utente ha zoomato, lo swipe serve per spostarsi, non per cambiare PDF
            if (window.visualViewport && window.visualViewport.scale > 1.05) return;
            
            if (touchendX < touchstartX - 60) nextPdf();
            if (touchendX > touchstartX + 60) prevPdf();
        }
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('pdf-modal');
            if (modal) {
                modal.addEventListener('touchstart', e => { 
                    if (e.changedTouches.length === 1) touchstartX = e.changedTouches[0].screenX; 
                }, {passive: true});
                modal.addEventListener('touchend', e => { 
                    if (e.changedTouches.length === 1) {
                        touchendX = e.changedTouches[0].screenX; 
                        handlePdfSwipe(); 
                    }
                }, {passive: true});
            }
        });'''

new_swipe = '''        let touchstartX = 0;
        let touchendX = 0;
        let isPinching = false;
        function handlePdfSwipe() {
            if (isPinching) return;
            if (currentPlaylist.length <= 1) return;
            if (window.visualViewport && window.visualViewport.scale > 1.05) return;
            
            if (touchendX < touchstartX - 60) nextPdf();
            if (touchendX > touchstartX + 60) prevPdf();
        }
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('pdf-modal');
            if (modal) {
                modal.addEventListener('touchstart', e => { 
                    if (e.touches.length > 1) isPinching = true;
                    if (e.touches.length === 1 && !isPinching) touchstartX = e.touches[0].screenX; 
                }, {passive: true});
                
                modal.addEventListener('touchmove', e => {
                    if (e.touches.length > 1) isPinching = true;
                }, {passive: true});
                
                modal.addEventListener('touchend', e => { 
                    if (e.touches.length === 0) { // tutte le dita sollevate
                        if (!isPinching && e.changedTouches.length === 1) {
                            touchendX = e.changedTouches[0].screenX; 
                            handlePdfSwipe(); 
                        }
                        setTimeout(() => { isPinching = false; }, 300);
                    }
                }, {passive: true});
            }
        });'''

content = content.replace(old_swipe, new_swipe)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully.")
