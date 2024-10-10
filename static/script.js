
function togglePump(pumpId) {
    fetch(`/toggle/${pumpId}`)
        .then(response => response.json())
        .then(data => {
            updatePumpStatus(data.status, data.time_on);
        });
}

function updatePumpStatus(status, time_on) {
    const pumpElements = document.querySelectorAll('.pump');
    const pumpTableRows = document.querySelectorAll('#pump-table tbody tr');

    pumpElements.forEach((pump, index) => {
        const statusElement = pump.querySelector('.status');

        //trạng thái trong bảng
        const pumpStatusCell = pumpTableRows[index].querySelector('.pump-status');

        var toggleButton = pump.querySelector('.toggle-btn');

        if (status[index]) {
            statusElement.textContent = 'Bật';
            toggleButton.classList.add('on');

            // Cập nhật trạng thái trong bảng
            pumpStatusCell.textContent = 'Bật';
            
        } else {
            statusElement.textContent = 'Tắt';
            toggleButton.classList.remove('on');

            // Cập nhật trạng thái trong bảng
            pumpStatusCell.textContent = 'Tắt';
        }

        // Cập nhật thời gian bật trong bảng
        const pumpTimeCell = pumpTableRows[index].querySelector('.pump-time');
        pumpTimeCell.textContent = time_on[index].toFixed(2); // Làm tròn đến 2 chữ số thập phân
    });
}

// Xuất dữ liệu ra file Excel
function exportData() {
    window.open('/export');
}

// Lấy trạng thái và thời gian bật của máy bơm khi tải trang
window.onload = function() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            updatePumpStatus(data.status, data.time_on);
        });
}
