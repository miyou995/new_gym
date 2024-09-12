var selectedEvents = []; // Declare globally

function initHTMXCalendar(eventsData) {
    console.log("init >>>>>>>>>>> initHTMXCalendar------<")

    // Reset selected events array when re-rendering the calendar
    selectedEvents = [];

    var typeAbonnement = document.getElementById("abonnement-select").value;
    console.log("Selected Type Abonnement Value:", typeAbonnement);

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
                info.el.classList.add('selected-event'); // Add selected state
            } else {
                selectedEvents.splice(index, 1);
                info.el.classList.remove('selected-event'); // Remove selected state
            }
            updateSidebar(selectedEvents); // Update sidebar with the selected events
        }
    });

    console.log("THE CALENDAR IS ------->", calendar);
    
    calendar.render();
}

function updateSidebar(selectedEvents) {
    console.log("updateside")

    var addAbonnementBtn = document.getElementById('add-abonnement-btn');
    if (selectedEvents.length > 0) {
        var eventPks = selectedEvents.map(event => event.event_pk);
        var today = document.getElementById('debut_date').value; // Get the selected date

        addAbonnementBtn.setAttribute('hx-vals', JSON.stringify({
            'event_pk': eventPks,
            'type_abonnement': document.getElementById("abonnement-select").value,
            'today': today
        }));
    } else {
        addAbonnementBtn.removeAttribute('hx-vals');
    }
}

function preInitHTMXCalendar() {
    console.log("date calender")
    const eventsBlock = document.querySelector("#eventsId");
    const events = JSON.parse(eventsBlock.dataset.events);
    
    initHTMXCalendar(events);

    var today = new Date();
    var formattedDate = today.toISOString().split('T')[0];
    document.getElementById('debut_date').value = formattedDate;

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
        } else if (selectedEvents.length === 0) {
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
