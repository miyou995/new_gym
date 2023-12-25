import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown } from "react-bootstrap";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
/// images
import {notifySuccess, notifyError} from '../Alert'
import Autocomplete from '@material-ui/lab/Autocomplete';
import { Link } from "react-router-dom";


import PresenceEditModal from './PresenceEditModal'
import PresenceCreateModal from './PresenceCreateModal'
import TextField from '@material-ui/core/TextField';
import useAxios from "../useAxios";
import useAuth from "../useAuth";
import Error403 from "../../pages/Error403";

// import axiosInstance from "../../axiosApi";

export const ClientContext = React.createContext()
function refreshPage() {
   window.location.reload(false);
 }


const PresenceList = () => {
   const api = useAxios();


   const [editModal, setEditModal] = useState(false);
   const [presneceCreateModal, setPresneceCreateModal] = useState(false);
   const [nextpage, setNextpage] = useState(1);
   const [client, setClient ] = useState('')
   const [carteClient, setCarteClient ] = useState('')
   
   const [clientId, setClientId ] = useState('')
   const [presenceId, setPresenceId ] = useState('')
   const [hourIn, setHourIn ] = useState('') 
   const [hourOut, setHourOut ] = useState('') 
   const [creneau,setCreneau] = useState('')
   const [note, setNote] = useState('')
   const [date, setDate] = useState('')
   const [activity, setActivity] = useState('')
   const [filterActivity, setFilterActivity] = useState('')
   const [presenceSuccess, setPresenceSuccess] = useState(false);
   const [presenceError, setPresenceError] = useState(false);
   const [presenceupdatedSuccess, setPresenceupdatedSuccess] = useState(false);
   const [presenceCreatedSuccess, setPresenceCreatedSuccess] = useState(false);
   const [searchValue, setSearchValue] = useState('')
   const [searchBarActivated, setSearchBarActivated] = useState(false)
   const [presenceData, setPresenceData] = useState([]);
   const [sallesData, setSallesData] = useState([]);
   const [activities, setActivities] = useState([]);
   const [presencesCount, setPresencesCount] = useState('')
   
   

   // console.table('els clieeents', salle);

   // const capitalizeFirstLetter = (word) => {
   //    if (word)
   //    return word.charAt(0).toUpperCase() + word.slice(1);
   //    return '';
   // };
   // //console.log('le clieeeeen RFID', client);
// 

   const formatDate = (date) => {
      try {
         const returned = new Date(date).toISOString().slice(0, 10)
         return returned
      } catch (error) {
         const returned = new Date().toISOString().slice(0, 10)
         return returned
      }
   }

   const [startDate, setStartDate] = useState(formatDate(new Date('2000-01-01')));
   const [endDate, setEndDate] = useState(formatDate(new Date()));
   const [salleId, setSalleId] = useState('');
   const [startHour, setStartHour] = useState('');
   // const sallesData = useGetAPI(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`)
   // const activities = useGetAPI(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`)
   let presenceCreateEND =  `${process.env.REACT_APP_API_URL}/rest-api/presence/auto-create`
   
   const [salleStatus, setSalleStatus] = useState(null)
   
   useEffect(() => {
      api.get(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`).then( res=> {
         setSallesData(res.data)
         setSalleStatus(res.status)
      }).catch(err => {
         setSalleStatus(err.response.status)
      })
      api.get(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`).then( res=> {
         setActivities(res.data)
      }) 
   }, []);

const getCurrentDay = (PresneceDate) => {
   const date = new Date(PresneceDate).getDay()

   if (date === 0) {
      return 'Dimanche'
   }else if (date === 1){
      return 'Lundi'

   }else if (date === 2){
      return 'Mardi'

   }else if (date === 3){
      return 'Mercredi'

   }else if (date === 4){
      return 'Jeudi'

   }else if (date === 5){
      return 'Vendredi'
   }else {
      return 'Samedi'
   }
} 

const [presenceStatus, setPresenceStatus] = useState(null);

   
   useEffect(() => {
      const presenceDateDate = async () => {
         const dateDebut = formatDate(startDate)
         const dateFin = formatDate(endDate)
         const endpoint = `${process.env.REACT_APP_API_URL}/rest-api/presence/?page=${nextpage}&start_date=${dateDebut}&end_date=${dateFin}&abc__client_id=${searchValue}&creneau__activity__salle=${salleId}&hour=${startHour}&creneau__activity=${filterActivity}`

         // const result =  await api.get(`${process.env.REACT_APP_API_URL}/rest-api/presence/?page=${nextpage}&start_date=${dateDebut}&end_date=${dateFin}&abc__client_id=${searchValue}&creneau__activity__salle=${salleId}&hour=${startHour}&creneau__activity=${filterActivity}`)
         // //console.log('cest un result ', result);
         // setPresenceData(result.data.results)
         // setPresencesCount(result.data.count)
         await api.get(endpoint)
         .then(res => {
            setPresenceData(res.data.results)
            setPresencesCount(res.data.count)
            setPresenceStatus(res.status)
         }).catch(err => {
            console.log(err);
            setPresenceStatus(err.response.status)
         })
      }
      presenceDateDate()
   }, [startDate, endDate, clientId,nextpage, searchValue, client, presenceCreatedSuccess, presenceupdatedSuccess, salleId, editModal, presneceCreateModal, startHour, filterActivity]);

// const HandleSubmit = (e) => {
//    e.preventDefault();
//    const presenceData =  api.get(`${process.env.REACT_APP_API_URL}/rest-api/get-client/?cl=${clientId}`).then(
//       res=> {
//       if (res.data.last_presence) {
//          setPresenceId(res.data.last_presence)
//          api.put( `${process.env.REACT_APP_API_URL}/rest-api/presence/edit/${res.data.last_presence}/`)
//          notifySuccess(`la sortie de ${clientId} a été éffectué Avec Succée`)
//          setClientId('')
//          // console.log('presenceData', presenceData);
//          return presenceData
//       } else {
//          try {
//             const presenceData1 = api.post(presenceCreateEND,{client: clientId}).then(res => {
//                notifySuccess(`Entrée autorisée, ${clientId}`)
//                setClientId('')
//             })
//             return presenceData1
//          } catch (error) {
//             notifyError("Erreur, Entrée non autorisée")
//          }} 
//    }).catch(err => {
//       console.log(err);
//       notifyError("Cet ID n'existe pas dans nos fichier")
//    })
// }

const HandleSubmit = (e) => {
   e.preventDefault();
   const presenceData =  api.get( `${process.env.REACT_APP_API_URL}/rest-api/client-auto-presence/${clientId}`).then(res=> {
         console.log("24 kara ", res.data);
         if (res.data.status === "error") {
            console.log("res.data.message", res.data.message);
            setClientId('')
            //          notifySuccess(`la sortie de ${clientId} a été éffectué Avec Succée`)
            notifyError(res.data.message)
         }else{
            console.log("erhaba a baba", res.data.message);
            //          notifySuccess(`la sortie de ${clientId} a été éffectué Avec Succée`)
            notifySuccess(res.data.message)
            setClientId('')
         }
      }).catch(error  => {
         console.log("24 error .data ", error );
         console.log("Error: ", error.response.data.error);
         // console.log(res.error);
         notifyError(error.response.data.error)
   })
}


const presenceAuthorization = `${process.env.REACT_APP_API_URL}/rest-api/presence/`

const [presenceAuth, loading] = useAuth(presenceAuthorization, 'GET')


   return (
      <Fragment>
      { loading &&
         <>
         {presenceAuth ? (
         <>
         <Link target="_blank" to={`/client/${clientId}`} >
            <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
         </Link>
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div> 

         <div className="m-5 row">
            <div className='col- col-md-4'>
               <form onSubmit={HandleSubmit}>
                  <div className='row'>
                     <div className="col-6">
                     <label htmlFor="entree">Présence Automatique </label>
                        <input id="presenceInput" name='entree' type="text" className="form-control" value={clientId} placeholder="ID Client" onChange={e =>  setClientId(e.target.value)} />
                     </div>
                     <div className="col-6 mt-auto">
                        <Button  variant="success" type="submit" > Valider</Button>
                     </div>
                  </div>
               </form>
            </div> 
            <div className="col-md-2 mt-auto">
               <Button  variant="primary" type="submit" onClick={e => setPresneceCreateModal(true)}> Présence Manuelle</Button>
            </div>
            <div  className="ml-auto col-md-2">
               <h2 className='text-danger'>Total :{presencesCount}</h2>
            </div>
         </div>
         <div className="row d-flex m-3 py-4" style={{backgroundColor:'#ffffff'}}>
            <div className=" col-md-2">
               <label style={{color:'#000000'}} >ID Adhérant</label>
               <input type="text" className="form-control" placeholder="rechercher par ID Client" value={searchValue} onChange={e => setSearchValue(e.target.value)}/>
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} >Salle d'activité</label>
                  <Autocomplete
                     // id={(option) =>  option['id']}
                     onChange={((event, value) =>  {
                        try {
                           setSalleId(value.id)
                        } catch (error) {
                           setSalleId('')
                        }
                     })}
                     // onChange={handleSubmit}
                     options={sallesData}
                     //  value={activities[creneauActivite]}
                     
                     getOptionSelected={(option) =>  option['id']}
                     getOptionLabel={(option) =>  option['name']}
                     style={{ color: '#000' }}
                     renderInput={(params) => 
                     <TextField {...params} style={{color:"#000"}}  className='text-light' label="Salles" variant="outlined" InputLabelProps={{style: { color: '#000' }, }}/>}
                  />

            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} >Activité</label>
               <Autocomplete
               // id={(option) =>  option['id']}
               onChange={((event, value) =>  {
                  try {
                     setFilterActivity(value.id)
                  } catch (error) {
                     setFilterActivity('')
                  }
               })}
               // onChange={handleSubmit}
               options={activities}
               style={{ color: '#000' }}
               //  value={activities[creneauActivite]}
               getOptionSelected={(option) =>  option['id']}
               getOptionLabel={(option) =>  option['name']}
               renderInput={(params) => 
                  <TextField {...params}  
                     InputLabelProps={{
                        style: { color: '#000' }, 
                     }}
                  style={{color:'#ffffff'}}  label="Activitées" variant="outlined" />}
               />
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="birth_date">Date début </label>
               <input type="date" name="start_date" className="form-control" value={startDate}  pattern="\d{1,2}/\d{1,2}/\d{4}" onChange={e => setStartDate(e.target.value)}/>
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="end_date">Date Fin </label>
               <input type="date" name="end_date" className="form-control" value={endDate} onChange={e => setEndDate(e.target.value)}/>
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="start_hour">Heure du créneau</label>
               <input type="time" name="start_hour" className="form-control" value={startHour} onChange={e => setStartHour(e.target.value)}/>
            </div>
         </div>
         <div className="row">
            <div className="col-lg-12">
               <div className="card">
                  <div className="card-body" style={{padding: '5px'}}>
                     <div className="table-responsive">
                        <table className="table mb-0 table-striped">
                           <thead>
                              <tr>
                                 <th className="customer_shop"> ID </th>
                                 <th>Nom</th>
                                 <th>Reste AB</th>
                                 <th>Activité</th>
                                 <th> Date </th>
                                 <th> Jour </th>
                                 <th className="pl-5 width200"> Heure d'entrée </th>
                                 <th> Heure de sortie </th>
                                 <th> Notes </th>
                                 <th className='text-right'>Dettes </th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                              {presenceData.map(presence => (
                                 <tr key={presence.id} className="btn-reveal-trigger cursor-abonnement presences p-0" onClick={e => {
                                    setEditModal(true)
                                    setClient(presence.client_last_name)
                                    setClientId(presence.client)
                                    setPresenceId(presence.id)
                                    setHourIn(presence.hour_entree)
                                    setHourOut(presence.hour_sortie)
                                    setCreneau(presence.creneau)
                                    setNote(presence.note)
                                    setDate(presence.date)
                                    setActivity(presence.activity)
                                 }}>
                                    <td className="customer_shop_single"> {presence.client} </td>
                                    <td className={`text-left ${presence.is_red}`}>{presence.seances}</td>

                                    <td className="">
                                       {/* <Link to={`/presence/detail/${presence.id}`}> */}
                                          <div className="media d-flex align-items-center">
                                             <div className="media-body">
                                                <h5 className="mb-0 fs--1">
                                                   {presence.client_last_name}
                                                </h5>
                                             </div>
                                          </div>
                                       {/* </Link> */}
                                    </td>
                                    <td >{presence.activity}</td>
                                    <td >{presence.date}</td>
                                    <td >{getCurrentDay(presence.date)}</td>
                                    <td className=" pl-5 wspace-no"> {presence.hour_entree} </td>
                                    <td >{presence.hour_sortie}</td>
                                    <td className=" text-left">{presence.note}</td>
                                    
                                    <td className=" text-right text-danger">{presence.dettes.reste__sum}</td>
                                 </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
            <PresenceEditModal show={editModal} onShowChange={setEditModal} presenceData={{presenceId:presenceId, client:client, hourIn:hourIn, hourOut: hourOut, creneau:creneau, note:note, clientId:clientId, date:date, activity:activity}}/>
            <PresenceCreateModal show={presneceCreateModal} onShowChange={setPresneceCreateModal} />
         </div>
         {
            !searchBarActivated &&
            <div className='d-flex text-center justify-content-end'>
               <div className='dataTables_info text-black' id='example5_info '>
                  {/* Showing {activePag.current * sort + 1} to{' '}
                  {data.length > (activePag.current + 1) * sort
                    ? (activePag.current + 1) * sort
                    : data.length}{' '}
                  of {data.length} entries{' '} */}
               </div>
               <div className='dataTables_paginate paging_simple_numbers' id='example5_paginate' >
                  <Button
                    onClick={() =>
                     nextpage > 0 && setNextpage(nextpage - 1)
                  }
                  style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'left', fontSize:'15px', paddingLeft:'8px'}}>
                    Précédent
                  </Button>
                  <span >
                      <input to='/transactions' type='number' className='paginate_button_client' onChange={e => setNextpage(e.target.value)} value={nextpage} style={{width: '100px', border: 'none', height:'99%', textAlign: 'center', fontSize:'15px', backgroundColor: '#ffffff'}}/>
                  </span>
                  <Button style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'center', fontSize:'15px', padding:'2px'}}
                    onClick={() =>
                     nextpage > 0 && setNextpage(Number(nextpage) + 1)
                    }
                  >
                    Suivant
                  </Button>
               </div>

            </div>
         }
         </>
         ) : <Error403 />}
      </>
      }
      </Fragment>
   );
};

export default PresenceList;
