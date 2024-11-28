var selectedEvents = []; // Declare globally
var deselectedEvents = []; 
var isAbonnementManuallyChanged = false;






function initHTMXCalendar(eventsData) {
    console.log("init >>>>>>>>>>> initHTMXCalendar------<")
    selectedEvents = [];
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
            var selectedEventsDiv = document.getElementById('eventsId');
            // console.log("selectedEventsDiv.dataset.selected>>>>>", selectedEventsDiv.dataset.selectedEvents);
            if (selectedEventsDiv) {
                var selectedEventsData = selectedEventsDiv.dataset.selectedEvents ? JSON.parse(selectedEventsDiv.dataset.selectedEvents) : [];
                selectedEvents = selectedEventsData.length > 0 ? selectedEventsData : [];
                console.log("Mounting selectedEvents----------", selectedEvents);
            }
            var preSelectedEvent = selectedEvents.find(event => event.creneaux__pk === info.event.extendedProps.pk_event);
            if (preSelectedEvent) {
                info.el.classList.add('selected-event');
            }
            addSelectedEventsVals(selectedEvents);

        },
        eventClick: function(info) { // info c'est creneau
            info.jsEvent.preventDefault();
            var selectedEvent = {
                creneaux__pk: info.event.extendedProps.pk_event,
                creneaux__name: info.event.title,
                creneaux__hour_start: info.event.start.toISOString(),
                creneaux__hour_finish: info.event.end.toISOString(),
                url: info.event.url
            };

            var index = selectedEvents.findIndex(event => {
                return event.creneaux__pk === info.event.extendedProps.pk_event;
            });
            if (index === -1) {
                info.el.classList.add('selected-event');
                selectedEvents.push(selectedEvent);
            } else {
                info.el.classList.remove('selected-event');
                selectedEvents.splice(index, 1);  // Remove event from selectedEvents
            }
            addSelectedEventsVals(selectedEvents);
        }
    });
    calendar.render();
}

function addSelectedEventsVals(selectedEvents) {
    var addAbonnementBtn = document.getElementById('add-abonnement-btn');
    
    if (selectedEvents.length > 0) {
        var eventPks = selectedEvents
            .filter(event => event.creneaux__pk && event.creneaux__pk !== 'null')  // Filter out null or invalid creneaux__pk
            .map(event => event.creneaux__pk);
            addAbonnementBtn.setAttribute('hx-vals', JSON.stringify({
                'event_pk': eventPks,
            }));
    } else {
        addAbonnementBtn.removeAttribute('hx-vals');
    }
}




function preInitHTMXCalendar() {
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









