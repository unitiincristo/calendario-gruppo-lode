import sys

html_file = 'index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openPdfModal
old_open = '''        function openPdfModal(playlistDataStr, index) {
            try {
                let decodedStr = playlistDataStr;
                if (playlistDataStr.startsWith('%5B')) {
                    decodedStr = decodeURIComponent(playlistDataStr);
                }

                if (decodedStr.startsWith('[')) {
                    currentPlaylist = JSON.parse(decodedStr);
                    currentPdfIndex = index;
                } else {
                    // Backward compatibility (e.g. from Canzoni list)
                    currentPlaylist = [{url: playlistDataStr, title: index}]; 
                    currentPdfIndex = 0;
                }
            } catch (e) {
                console.error("Error parsing playlist", e);
                return;
            }
            
            const modal = document.getElementById('pdf-modal');
            document.body.style.overflow = 'hidden';
            
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) viewport.setAttribute("content", "width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes");
            
            renderCurrentPdf();
            modal.classList.remove('hidden');
            
            if (window.visualViewport) {
                updateFloatingButtons();
                window.visualViewport.addEventListener('resize', updateFloatingButtons);
                window.visualViewport.addEventListener('scroll', updateFloatingButtons);
            }
        }'''

new_open = '''        function openPdfModal(playlistDataStr, index) {
            try {
                let decodedStr = playlistDataStr;
                if (playlistDataStr.startsWith('%5B')) {
                    decodedStr = decodeURIComponent(playlistDataStr);
                }

                if (decodedStr.startsWith('[')) {
                    currentPlaylist = JSON.parse(decodedStr);
                    currentPdfIndex = index;
                } else {
                    currentPlaylist = [{url: playlistDataStr, title: index}]; 
                    currentPdfIndex = 0;
                }
            } catch (e) {
                console.error("Error parsing playlist", e);
                return;
            }
            
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) viewport.setAttribute("content", "width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes");
            
            // Nascondiamo l'intera app tranne il modale
            document.querySelectorAll('header, main, aside, #sidebar-overlay').forEach(el => {
                if (el.id !== 'pdf-modal') el.style.display = 'none';
            });
            
            const modal = document.getElementById('pdf-modal');
            modal.classList.remove('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.add('block', 'min-h-screen', 'bg-white');
            document.body.style.overflow = 'auto'; // Lascia fare lo scroll nativo al body
            
            renderCurrentPdf();
            
            if (window.visualViewport) {
                updateFloatingButtons();
                window.visualViewport.addEventListener('resize', updateFloatingButtons);
                window.visualViewport.addEventListener('scroll', updateFloatingButtons);
            }
        }'''

content = content.replace(old_open, new_open)

# 2. Update closePdfModal
old_close = '''        function closePdfModal() {
            const modal = document.getElementById('pdf-modal');
            document.body.style.overflow = '';
            
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) viewport.setAttribute("content", "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no");
            
            if (window.visualViewport) {
                window.visualViewport.removeEventListener('resize', updateFloatingButtons);
                window.visualViewport.removeEventListener('scroll', updateFloatingButtons);
            }
            
            modal.classList.add('hidden');
            const container = document.getElementById('pdf-container');
            Array.from(container.querySelectorAll('canvas')).forEach(c => c.remove());
        }'''

new_close = '''        function closePdfModal() {
            const modal = document.getElementById('pdf-modal');
            modal.classList.add('hidden', 'fixed', 'inset-0', 'z-[100]', 'flex', 'flex-col');
            modal.classList.remove('block', 'min-h-screen', 'bg-white');
            
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) viewport.setAttribute("content", "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no");
            
            if (window.visualViewport) {
                window.visualViewport.removeEventListener('resize', updateFloatingButtons);
                window.visualViewport.removeEventListener('scroll', updateFloatingButtons);
            }
            
            const container = document.getElementById('pdf-container');
            Array.from(container.querySelectorAll('canvas')).forEach(c => c.remove());
            
            // Ripristiniamo l'app
            document.querySelectorAll('header, main, aside, #sidebar-overlay').forEach(el => {
                if (el.id !== 'pdf-modal') el.style.display = '';
            });
            
            // Forza il reset delle view corrette
            let view = 'calendario';
            if (!document.getElementById('view-mansioni').classList.contains('hidden')) view = 'mansioni';
            if (!document.getElementById('view-canzoni').classList.contains('hidden')) view = 'canzoni';
            switchView(view);
            window.scrollTo(0, 0);
        }'''

content = content.replace(old_close, new_close)

# 3. Update pdf-container styles
old_container = '''<div class="flex-1 w-full bg-[#111111] overflow-auto relative touch-pan-x touch-pan-y bg-white" id="pdf-container">'''
new_container = '''<div class="w-full relative bg-white pb-20" id="pdf-container">'''
content = content.replace(old_container, new_container)

# 4. Update pdf-modal-header to be sticky
old_header = '''<div id="pdf-modal-header" class="flex items-center justify-between bg-[#111111] p-4 border-b border-[#333333] touch-pan-y">'''
new_header = '''<div id="pdf-modal-header" class="flex items-center justify-between bg-[#111111] p-4 border-b border-[#333333] sticky top-0 z-[110] w-full">'''
content = content.replace(old_header, new_header)

# 5. Update pdf-modal-footer to be sticky at bottom
old_footer = '''<div id="pdf-modal-footer" class="hidden items-center justify-between bg-[#111111] p-3 border-t border-[#333333] touch-pan-y">'''
new_footer = '''<div id="pdf-modal-footer" class="hidden items-center justify-between bg-[#111111] p-3 border-t border-[#333333] fixed bottom-0 left-0 w-full z-[110]">'''
content = content.replace(old_footer, new_footer)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully.")
