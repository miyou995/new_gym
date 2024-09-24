var selectedEvents = []; // Declare globally
var deselectedEvents = []; 
var isAbonnementManuallyChanged = false;

function initHTMXCalendar(eventsData) {
    console.log("init >>>>>>>>>>> initHTMXCalendar------<")
    // add abonnemet Client
    var typeAbonnement = document.getElementById("abonnement-select").value;
    console.log("Selected Type Abonnement Value:", typeAbonnement);

    var today = new Date();
    var formattedDate = today.toISOString().split('T')[0];
    document.getElementById('debut_date').value = formattedDate;

    // update abonnement Client :
    selectedEvents = [];
    var selectedEventsDiv = document.getElementById('selected_eventsID');
    if (selectedEventsDiv) {
        var selectedEventsData = selectedEventsDiv.dataset.events ? JSON.parse(selectedEventsDiv.dataset.events) : [];
        selectedEvents = selectedEventsData.length > 0 ? selectedEventsData : [];
        console.log("selectedEvents----------", selectedEvents);

        var date = selectedEvents.find(event => event.start_date !== undefined);
        if (date && date.start_date) {
            var dateSelect = document.getElementById("debut_date");
            dateSelect.value = date.start_date;
            console.log("start_date/*/*/*/*/*/---:", date.start_date);
        }
        // Only run the automatic abonnement selection if it hasn't been manually changed
        if (!isAbonnementManuallyChanged) {
            var abcd = selectedEvents.find(event => event.type_abonnement !== undefined);
            if (abcd && abcd.type_abonnement) {
                var abonnementSelect = document.getElementById("abonnement-select");
                abonnementSelect.value = abcd.type_abonnement;
                console.log("Type Abonnement automatically selected:", abcd.type_abonnement);
            }
        }
  
    }

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: '' // Disable other views to enforce the one-week display
        },
        slotMinTime: '06:00:00',
        slotDuration: '01:00:00',
        events: eventsData,
        selectable: true,
        eventDidMount: function(info) {
            var preSelectedEvent = selectedEvents.find(event => event.creneaux__pk === info.event.extendedProps.pk_event);
            if (preSelectedEvent) {
                info.el.classList.add('selected-event');
            }
        },
        eventClick: function(info) {
            info.jsEvent.preventDefault();
            var selectedEvent = {
                event_pk: info.event.extendedProps.pk_event,
                title: info.event.title,
                startTime: info.event.start.toISOString(),
                endTime: info.event.end.toISOString(),
                url: info.event.url
            };
            var index = selectedEvents.findIndex(event => event.url === selectedEvent.url);
            if (index === -1) {
                selectedEvents.push(selectedEvent);
                deselectedEvents = deselectedEvents.filter(event => event.url !== selectedEvent.url); // Remove from deselected if it was previously there
                info.el.classList.add('selected-event');
            } else {
                selectedEvents.splice(index, 1);  // Remove event from selectedEvents
                deselectedEvents.push(selectedEvent);  // Add event to deselectedEvents
                info.el.classList.remove('selected-event');
            }
            updateSidebar(selectedEvents, deselectedEvents);
        }
    });
    calendar.render();
}
function updateSidebar(selectedEvents, deselectedEvents) {
    console.log("updateside");
    var addAbonnementBtn = document.getElementById('add-abonnement-btn');
    if (selectedEvents.length > 0 || deselectedEvents.length > 0) {
        // Only select events with a valid event_pk
        var eventPks = selectedEvents
            .filter(event => event.event_pk && event.event_pk !== 'null')  // Filter out null or invalid event_pk
            .map(event => event.event_pk);
        
        var deselectedEventPks = deselectedEvents
            .filter(event => event.event_pk && event.event_pk !== 'null')  // Filter out null or invalid event_pk
            .map(event => event.event_pk);

        if (eventPks.length > 0 || deselectedEventPks.length > 0) {
            var today = document.getElementById('debut_date').value; // Get the selected date
            addAbonnementBtn.setAttribute('hx-vals', JSON.stringify({
                'event_pk': eventPks,
                'deselected_event_pk': deselectedEventPks,  // Send deselected event_pk
                'type_abonnement': document.getElementById("abonnement-select").value,
                'today': today
            }));
        } else {
            addAbonnementBtn.removeAttribute('hx-vals');
        }
    } else {
        addAbonnementBtn.removeAttribute('hx-vals');
    }
}


function preInitHTMXCalendar() {
    console.log("date calender");
    const eventsBlock = document.querySelector("#eventsId");
    const events = JSON.parse(eventsBlock.dataset.events);
    initHTMXCalendar(events);

    var addAbonnementBtn = document.getElementById('add-abonnement-btn');
    addAbonnementBtn.addEventListener('click', function(event) {
        if (!document.getElementById("abonnement-select").value) {
            // Show custom styled alert using SweetAlert
            Swal.fire({
                icon: 'warning',
                title: 'Error',
                text: 'Veuillez choisir un abonnement type.',
                confirmButtonText: 'OK'
            });
            event.preventDefault();  // Prevent form submission
        } else if (selectedEvents.length === 0 || deselectedEvents.length === selectedEvents.length) {
            // Ensure that at least one event is selected
            Swal.fire({
                icon: 'warning',
                title: 'Error',
                text: 'Veuillez choisir un créneau ou des créneaux.',
                confirmButtonText: 'OK'
            });
            event.preventDefault();  // Prevent form submission
        }
    });
}









