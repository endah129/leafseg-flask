document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('fileInput');
    const fileNameText = document.getElementById('file-name-text');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const uploadForm = document.getElementById('uploadForm');

    // 1. Animasi Progress Bar (Mengisi otomatis saat halaman dimuat)
    const dataWidthEls = document.querySelectorAll('[data-width]');
    setTimeout(() => {
        dataWidthEls.forEach(el => {
            const w = parseInt(el.getAttribute('data-width')) || 0;
            el.style.width = w + '%';
        });
    }, 300);

    // 2. Event Klik untuk Memilih File
    dropZone.addEventListener('click', () => fileInput.click());

    // 3. Prevent Default Behavior untuk Drag & Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // 4. Visual Feedback saat Drag File di atas Area
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('bg-light', 'border-success');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('bg-light', 'border-success');
        }, false);
    });

    // 5. Handle Dropped Files
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            updatePreview(files[0]);
        }
    });

    // 6. Handle File Selection via Input
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            updatePreview(this.files[0]);
        }
    });

    // 7. Fungsi Update Preview Gambar sebelum Upload
    function updatePreview(file) {
        if (file) {
            fileNameText.innerHTML = `<strong>Terpilih:</strong> ${file.name}`;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('d-none');
                previewContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            };
            reader.readAsDataURL(file);
        }
    }

    // 8. Animasi saat Form di-Submit (Loading State)
    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            document.getElementById('loader').style.display = 'block';
            uploadForm.querySelector('button').style.display = 'none';
        });
    }
});

/**
 * 9. Fitur Eksport PDF (Professional Feature)
 * Fungsi ini dipanggil melalui atribut onclick pada tombol di HTML
 */
function generatePDF() {
    const element = document.querySelector('.result-container-premium');
    const btn = event.currentTarget;
    
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Menyusun Laporan...';
    btn.disabled = true;

    const opt = {
        margin:       [0.2, 0.2], // Margin diperkecil agar pas
        filename:     `Laporan_LeafSeg_${new Date().getTime()}.pdf`,
        image:        { type: 'jpeg', quality: 1 },
        html2canvas:  { 
            scale: 2, 
            useCORS: true,
            scrollY: 0, // Kunci scroll agar tidak ada ruang kosong di atas
            windowWidth: document.documentElement.offsetWidth
        },
        jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' },
        pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] } // Mencegah pemotongan sembarangan
    };

    // Jalankan dengan promise untuk memastikan tombol kembali normal
    html2pdf().set(opt).from(element).save().then(() => {
        btn.innerHTML = '📄 Cetak Laporan PDF';
        btn.disabled = false;
    });
}