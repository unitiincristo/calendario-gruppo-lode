import sys

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openPdfModal to disable pull-to-refresh
old_open = '''            const modal = document.getElementById('pdf-modal');
            modal.classList.remove('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.add('block', 'min-h-screen', 'bg-white');
            document.body.style.overflow = 'auto'; // Lascia fare lo scroll nativo al body'''

new_open = '''            const modal = document.getElementById('pdf-modal');
            modal.classList.remove('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.add('block', 'min-h-screen', 'bg-white');
            document.body.style.overflow = 'auto'; // Lascia fare lo scroll nativo al body
            document.body.style.overscrollBehaviorY = 'none'; // Previene il pull-to-refresh'''

content = content.replace(old_open, new_open)

# 2. Update closePdfModal to re-enable pull-to-refresh
old_close = '''            modal.classList.add('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.remove('block', 'min-h-screen', 'bg-white');'''

new_close = '''            modal.classList.add('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.remove('block', 'min-h-screen', 'bg-white');
            document.body.style.overscrollBehaviorY = '';'''

content = content.replace(old_close, new_close)

# 3. Update handlePdfSwipe to support global swipe but disable on zoom
old_swipe = '''        let touchstartX = 0;
        let touchendX = 0;
        function handlePdfSwipe() {
            if (currentPlaylist.length <= 1) return;
            if (touchendX < touchstartX - 50) nextPdf();
            if (touchendX > touchstartX + 50) prevPdf();
        }
        document.addEventListener('DOMContentLoaded', () => {
            const header = document.getElementById('pdf-modal-header');
            const footer = document.getElementById('pdf-modal-footer');
            [header, footer].forEach(el => {
                if(!el) return;
                el.addEventListener('touchstart', e => { touchstartX = e.changedTouches[0].screenX; }, {passive: true});
                el.addEventListener('touchend', e => { touchendX = e.changedTouches[0].screenX; handlePdfSwipe(); }, {passive: true});
            });
        });'''

new_swipe = '''        let touchstartX = 0;
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

content = content.replace(old_swipe, new_swipe)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully.")
