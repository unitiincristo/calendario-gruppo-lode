import sys

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

old_swipe = '''        let touchstartX = 0;
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

new_swipe = '''        let touchstartX = 0;
        let touchstartY = 0;
        let touchendX = 0;
        let touchendY = 0;
        let isPinching = false;
        function handlePdfSwipe() {
            if (isPinching) return;
            if (currentPlaylist.length <= 1) return;
            if (window.visualViewport && window.visualViewport.scale > 1.05) return;
            
            const diffX = Math.abs(touchendX - touchstartX);
            const diffY = Math.abs(touchendY - touchstartY);
            
            // Se lo swipe è più verticale che orizzontale, ignoriamo
            if (diffY > diffX) return;
            
            if (touchendX < touchstartX - 60) nextPdf();
            if (touchendX > touchstartX + 60) prevPdf();
        }
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('pdf-modal');
            if (modal) {
                modal.addEventListener('touchstart', e => { 
                    if (e.touches.length > 1) isPinching = true;
                    if (e.touches.length === 1 && !isPinching) {
                        touchstartX = e.touches[0].screenX; 
                        touchstartY = e.touches[0].screenY;
                    }
                }, {passive: true});
                
                modal.addEventListener('touchmove', e => {
                    if (e.touches.length > 1) isPinching = true;
                }, {passive: true});
                
                modal.addEventListener('touchend', e => { 
                    if (e.touches.length === 0) { // tutte le dita sollevate
                        if (!isPinching && e.changedTouches.length === 1) {
                            touchendX = e.changedTouches[0].screenX; 
                            touchendY = e.changedTouches[0].screenY;
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
