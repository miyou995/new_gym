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
	



htmx.on("refresh_table", (event)=> {
	KTComponents.init();
console.log('refresh_table is triggering');

})

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

document.addEventListener('htmx:afterRequest', (event) => {
    if (event.detail.xhr.status === 204) {
        window.location.reload();
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

// $('#kt_calendar_modal').on('shown.bs.modal', function () {
//     console.log("OUIIIIIIIIIIIIIII MOOOON");
    
//     preInitHTMXCalendar();
// });

});