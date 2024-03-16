console.log("table.js loaded!");
function deleteRow(button) {
    var row = button.parentNode.parentNode; 
    var table = row.parentNode; 
    table.deleteRow(row.rowIndex); 
}

function updateTimeUntil() {
    var rows = document.querySelectorAll("table tr");
    var now = new Date();

    rows.forEach(function (row) {
        var dateCell = row.cells[3]; 
        
        
        if (!dateCell.hasAttribute("data-date")) {
            dateCell.setAttribute("data-date", dateCell.textContent);
        }

        var originalDateValue = Date.parse(dateCell.getAttribute("data-date"));

        if (!isNaN(originalDateValue)) {
            var timeDiff = originalDateValue - now;

            if (timeDiff <= 0) {
                dateCell.textContent = "PAST";
            } else {
                var seconds = Math.floor(timeDiff / 1000) % 60;
                var minutes = Math.floor(timeDiff / 1000 / 60) % 60;
                var hours = Math.floor(timeDiff / 1000 / 3600) % 24;
                var days = Math.floor(timeDiff / 1000 / 3600 / 24);
                dateCell.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
            }
        }
    });
}

function updateTimerInterval() {
    setInterval(updateTimeUntil, 1000);
}

updateTimeUntil();
updateTimerInterval();
