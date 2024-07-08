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


window.addEventListener("DOMContentLoaded", (e) => {
    console.log("loaded");
    recountForms()
})


document.addEventListener("htmx:load", function() {
    KTComponents.init();
});

document.addEventListener('htmx:afterRequest', (event) => {
    if (event.detail.xhr.status === 204) {
        window.location.reload();
    }
});
