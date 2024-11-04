htmx.on("closeModal", (event) => {
	
	if (event.detail.value) {
	var myModalEl = document.getElementById(event.detail.value);
	}else {
	var myModalEl = document.getElementById("kt_modal");
	}
	var modal = bootstrap.Modal.getInstance(myModalEl)
	// const modal = new bootstrap.Modal(document.getElementById("sg_create_modal"))
	console.log("closeModal",event.detail.value);
	console.log("modal",modal);
	if (modal) {
	console.log("LOGGING MODAL ", modal);
	modal.hide()
	} 
})
	



// htmx.on("refresh_table", (event)=> {
// 	KTComponents.init();
// console.log('refresh_table is triggering');

// })

htmx.onLoad(function(){
	KTComponents.init();
})

htmx.on('load', (e) => {
    KTComponents.init();
});




document.addEventListener('htmx:afterSettle', (e) => {
    console.log("htmx:afterSettle");
    const eventsBlock = document.querySelector("#eventsId");

    if (eventsBlock) {
        setTimeout(function(){
            console.log("HEEEY eventsId here HTMX REQUEST");
            preInitHTMXCalendar();
        },100)
    }
});

document.addEventListener('DOMContentLoaded', function () {
    console.log("Document loaaaded lets call the callendar");
    
    const eventsBlock = document.querySelector("#eventsId");
    if (eventsBlock) {
        console.log("HEEEY eventsId here HTTP REQUEST");
        preInitHTMXCalendar();
    }
});


document.addEventListener("htmx:load", function() {
    KTComponents.init();
});


// Store messages in localStorage before reload toastr
document.addEventListener('htmx:afterRequest', (event) => {
    if (event.detail.xhr.status === 204) {
        const trigger = event.detail.xhr.getResponseHeader('HX-Trigger');
        if (trigger) {
            const data = JSON.parse(trigger);
            if (data.messages) {
                localStorage.setItem('toastrMessages', JSON.stringify(data.messages));
            }
        }
        window.location.reload();
    }
});
window.addEventListener('load', () => {
    const toastrMessages = localStorage.getItem('toastrMessages');
    if (toastrMessages) {
        const messages = JSON.parse(toastrMessages);
        messages.forEach(msg => {
            if (msg.tags.includes('toastr')) {
                // Display Toastr notifications based on the message type
                if (msg.tags.includes('error')) {
                    toastr.error(msg.message);
                } else if (msg.tags.includes('warning')) {
                    toastr.warning(msg.message);
                } else if (msg.tags.includes('info')) {
                    toastr.info(msg.message);
                } else if (msg.tags.includes('success')) {
                    toastr.success(msg.message);
                }
            }
        });
        // Clear the stored messages to avoid showing them again
        localStorage.removeItem('toastrMessages');
    }
});




document.addEventListener('DOMContentLoaded', function () {
    const barcodeInput = document.getElementById('barcode-input');
    if (barcodeInput) {
        
    barcodeInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent the default action (form submission)
            handleSubmit();
        }
    });

    function handleSubmit() {
        const barcode = barcodeInput.value.trim();
        if (barcode) {
            // Trigger the HTMX request manually
            barcodeInput.dispatchEvent(new Event('keyup', { 'bubbles': true }));
        }
    }
}


});






window.addEventListener("DOMContentLoaded", (e) => {
	// const inputElements = document.getElementsByClassName('default-today');
	// inputElements.forEach(function(inputElement) {
	//   inputElement.value = today.toISOString().substring(0, 10);
	// });
	$('.affect-select').on('select2:select select2:unselect', function (e) {
	console.log("BOOM SELECT CHANGED");
		$(this).closest('select').get(0).dispatchEvent(new Event('change'));
	});
	$('.filter-select').on('select2:select select2:unselect', function (e) {
	console.log("BOOM SELECT CHANGED");
		$(this).closest('form').get(0).dispatchEvent(new Event('change'));
	});
});


window.addEventListener("DOMContentLoaded", (e) => {
	$('.warehouse-select').on('select2:select select2:unselect', function (e) {
		$('.products-select').trigger('change');
	});

});





var start = moment().subtract(29, "days");
var end = moment();

function cb(start, end) {
    $("#kt_daterangepicker_4").html(start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY"));
    console.log("date changes-----", document.querySelector('input[name="start_date"]').value);
    document.querySelector('input[name="start_date"]').value = start.format("YYYY-MM-DD");
    document.querySelector('input[name="end_date"]').value = end.format("YYYY-MM-DD");
    var chartContainers = document.querySelectorAll('.chart-container');
    
    // Trigger 'date_changed' event on each chart container
    chartContainers.forEach(function(el) {
        htmx.trigger(el, 'date_changed');
    });

}

$("#kt_daterangepicker_4").daterangepicker({
    startDate: start,
    endDate: end,
    ranges: {
        "aujourd'hui": [moment(), moment()],
        "hier": [moment().subtract(1, "days"), moment().subtract(1, "days")],
        "dernier 7 jours": [moment().subtract(6, "days"), moment()],
        "dernier 30 jours": [moment().subtract(29, "days"), moment()],
        "ce mois": [moment().startOf("month"), moment().endOf("month")],
        "mois dernier": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
    }
}, cb);


