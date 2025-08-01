// file: file_upload_preview.js
// Mở rộng trình tải tệp của Frappe để hiển thị ảnh thu nhỏ + tên file bên cạnh khi upload hình ảnh.
// Không thay đổi hành vi upload, validation hay event mặc định của Frappe.

(function() {
    /**
     * Đảm bảo có container để chứa preview, nếu chưa có thì tạo mới.
     * @param {HTMLInputElement} fileInput
     * @returns {HTMLElement} container preview
     */
    function ensurePreviewContainer(fileInput) {
        let container = fileInput.parentElement.querySelector(".custom-upload-preview");
        if (!container) {
            container = document.createElement("div");
            container.classList.add("custom-upload-preview");
            // Style cơ bản, có thể override thêm trong CSS
            container.style.display = "flex";
            container.style.gap = "0.5rem";
            container.style.marginTop = "0.5rem";
            fileInput.parentElement.appendChild(container);
        }
        return container;
    }

    /**
     * Xoá hết preview cũ trong container
     * @param {HTMLElement} container
     */
    function clearPreviews(container) {
        container.innerHTML = "";
    }

    /**
     * Tạo phần tử preview cho từng file
     * @param {File} file
     * @returns {HTMLElement} wrapper chứa thumbnail + tên file
     */
    function createFilePreview(file) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("custom-upload-preview-item");
        wrapper.style.display = "flex";
        wrapper.style.flexDirection = "column";
        wrapper.style.alignItems = "center";
        wrapper.style.fontSize = "0.85rem";

        // Nếu là ảnh, hiển thị thumbnail
        if (file.type.startsWith("image/")) {
            const img = document.createElement("img");
            img.classList.add("custom-upload-thumbnail");
            img.style.width = "80px";
            img.style.height = "80px";
            img.style.objectFit = "cover";
            img.src = URL.createObjectURL(file);
            img.onload = () => URL.revokeObjectURL(img.src);
            wrapper.appendChild(img);
        }

        // Luôn hiển thị tên file
        const nameDiv = document.createElement("div");
        nameDiv.classList.add("custom-upload-filename");
        nameDiv.textContent = file.name;
        nameDiv.style.marginTop = "0.25rem";
        wrapper.appendChild(nameDiv);

        return wrapper;
    }

    /**
     * Gắn preview khi input thay đổi (user chọn file)
     * @param {HTMLInputElement} fileInput
     */
    function attachPreviewToInput(fileInput) {
        const files = fileInput.files;
        if (!files || files.length === 0) return;

        const container = ensurePreviewContainer(fileInput);
        clearPreviews(container);

        Array.from(files).forEach(file => {
            const preview = createFilePreview(file);
            container.appendChild(preview);
        });
    }

    /**
     * Khởi tạo: tìm tất cả input[type=file] và gắn sự kiện change
     */
    function init() {
        document.querySelectorAll('input[type="file"]').forEach(input => {
            if (input.dataset.previewBound) return; // chỉ bind 1 lần
            input.addEventListener("change", () => attachPreviewToInput(input));
            input.dataset.previewBound = "true";
        });
    }

    // Nếu Frappe đã sẵn sàng, đợi frappe.ready(), ngược lại đợi DOMContentLoaded
    if (window.frappe && frappe.ready) {
        frappe.ready(init);
    } else {
        document.addEventListener("DOMContentLoaded", init);
    }
})();
