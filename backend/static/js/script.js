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


