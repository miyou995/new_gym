
    var selectedEvents = [];
    var typeAbonnement = "{{ type_abonnement|escapejs }}"; // Ensure type_abonnement is safely escaped for JS

    function initHTMXCalendar(eventsData) {
        console.log("init >>>>>>>>>>> initHTMXCalendar------<")

        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek', // Set the initial view to one week
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
                    info.el.classList.add('selected-event'); // Add shadow to the selected event
                } else {
                    selectedEvents.splice(index, 1);
                    info.el.classList.remove('selected-event'); // Remove shadow from the deselected event
                }
                updateSidebar(selectedEvents); // Update the sidebar with the selected events
            }
        });
        console.log("THE CALENDAR IS ------->",calendar);
        
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
                'type_abonnement': typeAbonnement,
                'today':today 
            }));
        } else {
            addAbonnementBtn.removeAttribute('hx-vals');
        }
    }

   
function preInitHTMXCalendar(selectedEvents) {

    console.log("date calender")
    const eventsBlock = document.querySelector("#eventsId");
    // console.log(eventsBlock);
    const events = JSON.parse(
        eventsBlock.dataset.events
      );
    const selectEvent = document.getElementById("#selectId");
    console.log("selectEvent",selectEvent)
      
    
    // const events = eventsBlock.dataset.events
    initHTMXCalendar(events);

    
    // initHTMXCalendar({{ events|safe }});

    var today = new Date();
        var formattedDate = today.toISOString().split('T')[0];
        document.getElementById('debut_date').value = formattedDate;
    //search without submit
    const form = document.getElementById('form_id');
    // if (form) {
        
    //     form.querySelectorAll('input, select, textarea').forEach(function(element) {
    //         element.addEventListener('change', function() {
    //             form.submit();
    //         });
    //     });
    // }

        //alert pour la selection de type abonnement
    form.addEventListener('add-abonnement-btn', function (event) {

            if (!typeAbonnement) {
                alert('veullez choisir an abonnement type.');
                event.preventDefault(); 
            }
        });
        var addAbonnementBtn = document.getElementById('add-abonnement-btn');
        addAbonnementBtn.addEventListener('click', function(event) {
            if (!typeAbonnement || typeAbonnement === "None") {
                // Show custom styled alert using SweetAlert
                Swal.fire({
                    icon: 'warning',
                    title: 'Error',
                    text: 'veullez choisir an abonnement type.',
                    confirmButtonText: 'OK'
                });
                event.preventDefault();  // Prevent form submission
            } else if (selectedEvents.length === 0) {
                // Ensure that at least one event is selected
                Swal.fire({
                    icon: 'warning',
                    
                    title: 'Error',
                    text: 'veullez choisir un creneau ou des creneaux  .',
                    confirmButtonText: 'OK'
                });
                event.preventDefault();  // Prevent form submission
            }
        });
    };


