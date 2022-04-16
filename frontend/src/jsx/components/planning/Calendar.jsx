import React, { useState , useEffect} from "react";
import { useGetAPI } from '../useAPI'
import axios from 'axios';
import CreneauEditModal from './CreneauEditModal';
import CreneauCreateModal from './CreneauCreateModal';
import ShortCuts from "../ShortCuts";
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
// import RefreshIcon from '@mui/icons-material/Refresh';
import {Col,Card,Table,} from "react-bootstrap";
import { ToastContainer } from 'react-toastify'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export const ModalState = React.createContext()


let sallesEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`
let coachEnd = `${process.env.REACT_APP_API_URL}/rest-api/coachs/`
let planningEND = `${process.env.REACT_APP_API_URL}/rest-api/planning/`
let defaultSalleIdEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/default_salle/`
let defaultPlanningIdEnd = `${process.env.REACT_APP_API_URL}/rest-api/planning/default_planning/`
let activitiesEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`

const Calendar = () => {
  const activities = useGetAPI(activitiesEnd)
  const coachs = useGetAPI(coachEnd)
  const plannings = useGetAPI(planningEND)
  const salles = useGetAPI(sallesEnd)
  // const defaultSalleGet = useGetAPI(defaultSalleIdEnd)
  // const defaultPlanningGet = useGetAPI(defaultPlanningIdEnd)
  const [modal, setModal] = useState(false);
  const [modalCreate, setModalCreate] = useState(false);

  const [salleId, setSalleId] = useState('');
  const [defaultSalle, setDefaultSalle] = useState("");
  const [defaultPlanning, setDefaultPlanning] = useState("");

  const [planningId, setPlanningId] = useState("");
  // const [salles, setSalles] = useState([]);

  const [samedi, setSamedi] = useState([]);
  const [dimanche, setDimanche] = useState([]);
  const [lundi, setLundi] = useState([]);
  const [mardi, setMardi] = useState([]);
  const [mercredi, setMercredi] = useState([]);
  const [jeudi, setJeudi] = useState([]);
  const [vendredi, setVendredi] = useState([]);
  const [creneauName, setCreneauName] = useState("")
  const [creneauColor, setCreneauColor] = useState("")
  const [selectedCreneau, setSelectedCreneau] = useState("")
  const [creneauActi, setCreneauActi] = useState("")
  const [creneauCoach, setCreneauCoach] = useState("")
  const [creneauPlanning, setCreneauPlanning] = useState("")
  const [creneauDay, setCreneauDay] = useState("")
  const [creneau, setCreneau] = useState("")
  

  const [startHour, setStartHour] = useState("")
  const [endHour, setEndHour] = useState("")

  const [coachName, setCoachName] = useState("")
  const [activityName, setActivityName] = useState("")
  const [jour, setJour] = useState("")
  
  const [clients, setClients] = useState([])
// console.log('la sallels salles', salles);
// console.log('la sallels id', salle);
    let result1=[]
    let result2=[]
    let result3=[]
    let result4=[]
    let result5=[]
    let result6=[]
    let result7=[]

    const DAYS_CHOICES = [
      {day :'SA', label : 'Samedi'},
      {day :'DI', label : 'Dimanche'},
      {day :'LU', label : 'Lundi'},
      {day :'MA', label : 'Mardi'},
      {day :'ME', label : 'Mercredi'},
      {day :'JE', label : 'Jeudi'},
      {day :'VE', label : 'Vendredi'},
]

useEffect(() => {
  axios.get(defaultSalleIdEnd).then(function name(response) {
    setSalleId(response.data['default_salle'].id)
    setDefaultSalle(response.data['default_salle'])
  })
  axios.get(defaultPlanningIdEnd).then(function name(response) {
    setPlanningId(response.data['default_planning'].id)
    setDefaultPlanning(response.data['default_planning'])
  })
}, []);

useEffect(() => {
  console.log("salleId", salleId)
  console.log("planningId", planningId)
  const FetchData = () => {
      axios.get(`${process.env.REACT_APP_API_URL}/rest-api/creneau/by-salle-planning?sa=${salleId}&pl=${planningId}`)
    .then(function (response) {
      console.log('les creneaux ', response.data);
      response.data.forEach((req) => {
      if (req.day === "SA") {
          console.log('req.day', req.day);
          result1.push(req);
          }else if(req.day === "DI"){
            result2.push(req);
          }else if (req.day === "LU"){
            result3.push(req);
          }else if(req.day === "MA"){
            result4.push(req);
          }else if(req.day === "ME"){
            result5.push(req);
          }else if(req.day === "JE"){
            result6.push(req);
          }else if(req.day === "VE"){
            result7.push(req);
          }
      })
        setSamedi(result1)
        setDimanche(result2)
        setLundi(result3)
        setMardi(result4)
        setMercredi(result5)
        setJeudi(result6)
        setVendredi(result7)
      })
  }
  FetchData();
}, [modal, salleId, planningId]);

  console.log('selected  creneaux', selectedCreneau);


const handleSelectedCreneau = (day) => {
  setSelectedCreneau(day.id)
  setCreneau(day.id)
  setCreneauActi(getActivity(activities, day.activity))
  setCreneauCoach(getActivity(coachs, day.coach))
  setCreneauPlanning(getActivity(plannings, day.planning))
  setCreneauDay(getDay(DAYS_CHOICES, day.day))
  setStartHour(day.hour_start)
  setEndHour(day.hour_finish)
  setClients(day.clients)
  setCoachName(day.coach_name)
  setActivityName(day.activity_name)
  setJour(day.day)
  setModal(true) 
  setCreneauName(day.name)
  setCreneauColor(day.color)
  console.log('creneau ', day);
}

 const getActivity = (acti,creneauActi) => {
  for (let i = 0; i < acti.length; i++) {
    if (creneauActi == acti[i].id){
       return i
      }            
  }
}
const getDay = (days,creneauDay) => {
  for (let i = 0; i < days.length; i++) {
    if (creneauDay == days[i].day){
      console.log('the day is :', creneauDay);
       return i
      }            
  }
}
   return (
      <div className="h-80">
              <ToastContainer
                position='top-right'
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
         <div>
          <div className="row d-flex justify-content-between mb-5">
             <div className="col-4">
             <Autocomplete
                  options={plannings}
                  getOptionLabel={(option) => option.name || ''}
                  onChange={((event, value) =>  {
                    if (value) {
                      setPlanningId(value.id)
                      setDefaultPlanning(value)
                    }
                  })} 
                  renderInput={(params) => (<TextField {...params} name="planning" label="Plannings" variant="outlined" fullWidth />)}
                />
             </div>
             <div className="col-4">
             <Autocomplete
                    options={salles}
                    getOptionLabel={(option) => option.name || ''}
                    onChange={((event, value) =>  {
                    if (value) {
                      setSalleId(value.id)
                      setDefaultSalle(value)
                    }
                    })} 
                    renderInput={(params) => (<TextField {...params} name="salle" label="Salles" variant="outlined" fullWidth />)}
                />
              {/* <label>Salles</label>
              <select name="activities" defaultValue={salleId} className="form-control" onChange={e => setSalleId(e.target.value)  }>
                {salles.map( salle => (
                  <option key={salle.id} value={salle.id}>{salle.name}</option>
                ))}
              </select> */}
             </div>
            <div className="btn btn-primary m-3 ml-auto" onClick={e => setModalCreate(true)  }>+ Creneau</div>
          </div>
         <Col lg={12}>
         {/* <RefreshIcon /> */}
          <Card>
          <Card.Title className="text-center">Planning: {defaultPlanning.name} | salle de {defaultSalle.name}</Card.Title>
            {/* <Card.Body> */}
          <Table responsive bordered className="verticle-middle calendar">
            <tbody>
              { dimanche.length > 0 &&
                <tr>
                  <th style={{verticalAlign: "middle", width: "130px"}}>
                      <h4 className="pl-2 text-black">Dimanche</h4>
                  </th>
                  <td className ="d-flex">
                  { dimanche.map(day=> ( 
                    <div className ="ml-1" style={{border: "none"}}  key={day.id} id={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                          <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                          <ul className='text-left'>
                            <li>  {day.name ? day.name :day.coach_name }  </li>
                            <li> {day.clients_count} Abonné</li>
                            <li> {day.activity_name}</li>
                          </ul> 
                        </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { lundi.length > 0 &&
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                      <h4 className="pl-2 text-black">Lundi</h4>
                  </th>
                  <td  className ="d-flex" style={{ padding: '3px'}}>
                  { lundi.map(day=>   ( 
                    <div className ="ml-1" style={{border: "none"}} id={day.id} key={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                            <li> {day.coach_name}</li>
                            <li> {day.clients_count} Abonné</li>
                            <li>{day.activity_name}</li> 
                            </ul> 
                          </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { mardi.length > 0 &&
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                        <h4 className="pl-2 text-black">Mardi</h4>
                  </th>
                  <td className ="d-flex">
                  { mardi.map(day=>   ( 
                      <div className ="ml-1"  style={{border: "none"}} id={day.id}  key={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                            <li>  {day.name ? day.name :day.coach_name }</li>
                            <li> {day.clients_count} Abonné</li>
                            <li>{day.activity_name}</li>
                            </ul> 
                          </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { mercredi.length > 0 &&
                
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                        <h4 className="pl-2 text-black">Mercredi</h4>
                  </th>
                  <td className ="d-flex">
                  { mercredi.map(day=>   ( 
                      <div className ="ml-1" style={{border: "none"}}  id={day.id}  key={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                            <li>  {day.coach_name}</li>
                            <li> {day.clients_count} Abonné</li>
                            <li>{day.activity_name}</li>
                            </ul> 
                          </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { jeudi.length > 0 &&
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                        <h4 className="pl-2 text-black">Jeudi</h4>
                  </th>
                  <td className ="d-flex">
                  { jeudi.map(day=>   ( 
                      <div className ="ml-1"  style={{border: "none"}}  id={day.id}   key={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                            <li>  {day.coach_name}</li>
                            <li> {day.clients_count} Abonné</li>
                            <li>{day.activity_name}</li>
                            </ul> 
                          </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { vendredi.length > 0 &&
                
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                        <h4 className="pl-2 text-black">Vendredi</h4>
                  </th>
                  <td className ="d-flex">
                  { vendredi.map(day=>   ( 
                      
                      <div className ="ml-1" style={{border: "none"}}  id={day.id} key={day.id}  onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                            <li>  {day.coach_name}</li>
                            <li> {day.clients_count} Abonné</li>
                            <li>{day.activity_name}</li>
                            </ul> 
                          </div>
                      </div> 
                      ))}
                  </td>
                </tr>
              }
              { samedi.length > 0 &&
                <tr>
                  <th style={{verticalAlign: "middle"}}>
                      <h4 className="pl-2 text-black">Samedi</h4>
                  </th>
                  <td className ="d-flex">
                  { samedi.map(day=> ( 
                      <div className ="ml-1" style={{border: "none"}}  id={day.id}  key={day.id} onClick={() => handleSelectedCreneau(day)}>
                        <div className="fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded" style={{backgroundColor: day.creneau_color}}>
                            <h5> {day.hour_start}<span> - </span> {day.hour_finish}</h5> 
                            <ul className='text-left'>
                              <li> {day.coach_name}</li>
                              <li> {day.clients_count} Abonné</li>
                              <li> {day.activity_name}</li>
                            </ul> 
                          </div>
                      </div> 

                      ))}
                  </td>
                </tr>
              }
            </tbody>
          </Table>
            <div>
              <CreneauCreateModal show={modalCreate} onShowShange={setModalCreate} 
                creneauData={{
                creneauId : selectedCreneau,
                activite :creneauActi,
                activities : activities,
                coach : creneauCoach,
                planning: creneauPlanning,
                coachs: coachs,
                plannings: plannings,
                days : DAYS_CHOICES,
                day : creneauDay ,
                startHour: startHour,
                endHour: endHour, 
                clients : clients
                }} 
              />
              <CreneauEditModal show={modal} onShowShange={setModal} creneauData={{
                creneauId : selectedCreneau,
                activite :creneauActi,
                activities : activities,
                coach : creneauCoach,
                planning: creneauPlanning,
                coachs: coachs,
                plannings: plannings,
                days : DAYS_CHOICES,
                day : creneauDay ,
                startHour: startHour,
                endHour: endHour, 
                clients : clients,
                coachName : coachName,
                activityName : activityName,
                jour : jour,
                creneauName: creneauName,
                creneauColor: creneauColor,
                creneau: creneau
                }} />
              </div>
          </Card>
        </Col>
         </div>
      </div>
   );
};

export default Calendar;
