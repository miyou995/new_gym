
function createToast(message) {
    const element = htmx.find("[data-toast-template]").cloneNode(true)
    delete element.dataset.toastTemplate
    // console.log("INDEAAAD ITS TRIGGERED", message);
    // element.className += " bg-" + message.tags
    htmx.find(element, "[data-toast-body]").innerHTML = message.message
    // htmx.find(element, "[data-toast-header]").innerHTML = message.tags
    const header = htmx.find(element, "[data-toast-header]")
    header.classList.add("mystyle");
    htmx.find(element, "[data-toast-tags]").innerHTML = message.tags;
    htmx.find(header, ".ki-solid").className += " text-" + message.tags
    // htmx.find(element, "[data-toast-tags]").innerHTML = message.tags
    // element.classList.add("mystyle");
    // element.classList.add(`text-bg-${message.tags}`);
    // element.className += " bg-" + message.tags

    // htmx.addClass(htmx.find(element, "[data-toast-tags]"), `text-bg-${message.tags}`)
    
    htmx.find("[data-toast-container]").appendChild(element)
    const toast = new bootstrap.Toast(element)
    // console.log("The new element", element);
    // console.log("The new toast", toast);
    // console.log("The new toast isShown", toast.isShown());
    setTimeout(() => {
        toast.show();
        console.log("The new toast isShown-------2", toast.isShown());
    }, 100);
}


htmx.on("messages", (event) => {
    // console.log("MEssage receivedscsqcsq", event);
    event.detail.value.forEach(createToast)
})

