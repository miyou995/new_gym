import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown } from "react-bootstrap";
import useAxios from "../useAxios";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
/// images
import {notifySuccess, notifyError} from '../Alert'
import Autocomplete from '@material-ui/lab/Autocomplete';
import { Link } from "react-router-dom";


import TextField from '@material-ui/core/TextField';

export const ClientContext = React.createContext()
  const HistoryTrans = () => {
  const api = useAxios();
  const formatDate = (date) => {
      try {
         const returned = new Date(date).toISOString().slice(0, 10)
         return returned
      } catch (error) {
         const returned = new Date().toISOString().slice(0, 10)
         return returned
      }
   }
   // const getCurrentDay = (PresneceDate) => {
   //    const date = new Date(PresneceDate).getDay()
   
   //    if (date === 0) {
   //       return 'Dimanche'
   //    }else if (date === 1){
   //       return 'Lundi'
   
   //    }else if (date === 2){
   //       return 'Mardi'
   
   //    }else if (date === 3){
   //       return 'Mercredi'
   
   //    }else if (date === 4){
   //       return 'Jeudi'
   
   //    }else if (date === 5){
   //       return 'Vendredi'
   //    }else {
   //       return 'Samedi'
   //    }
   // } 
   // const [editModal, setEditModal] = useState(false);
   // const [presneceCreateModal, setPresneceCreateModal] = useState(false);
   const [nextpage, setNextpage] = useState(1);
   const [client, setClient ] = useState('')
   const [abcsData, setAbcsData] = useState([]);
   const [users, setUsers] = useState([]);
   const [userId, setUserId] = useState("");
   const [abcId, setAbcId] = useState("");

   const [requestedUrl, setRequestedUrl] = useState(null);
   const [nextUrl, setNextUrl] = useState("");
   const [previusUrl, setPreviusUrl] = useState("");

   const [searchValue, setSearchValue] = useState('')
   const [searchBarActivated, setSearchBarActivated] = useState(false)
   const [presenceData, setPresenceData] = useState([]);
   const [presencesCount, setPresencesCount] = useState('')
   const [startDate, setStartDate] = useState(formatDate(new Date('2000-01-01')));
   const [endDate, setEndDate] = useState(formatDate(new Date()));
   const [salleId, setSalleId] = useState('');
   const [startHour, setStartHour] = useState('');
   let usersEnd =  `${process.env.REACT_APP_API_URL}/rest-api/auth/users`

   // console.table('els clieeents', salle);

   // const capitalizeFirstLetter = (word) => {
   //    if (word)
   //    return word.charAt(0).toUpperCase() + word.slice(1);
   //    return '';
   // };
   // //console.log('le clieeeeen RFID', client);
// 


useEffect(() => {
   api.get(usersEnd).then(res => {
      setUsers(res.data.results)
      console.log("DATAAAA", res.data);
   })
}, [usersEnd])

useEffect(() => {
   api.get(`${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/history?cl=${searchValue}&abc=${abcId}&start=${startDate}&end=${endDate}&usr=${userId}`).then(res => {
      setAbcsData(res.data.results)
      setNextUrl(res.data.next) 
      setPreviusUrl(res.data.previous)
      //console.log('setAbcsData', res.data);
   })
}, [abcId, endDate, searchValue, startDate, userId])
useEffect(() =>  {
   if (requestedUrl) {
      api.get(requestedUrl).then(res => {
         //console.log('le resultat des clients est ', res);
         setAbcsData(res.data.results)
         setNextUrl(res.data.next)
         setPreviusUrl(res.data.previous)
         console.log('le setNextUrl des ', nextUrl);     
         console.log('le setPreviusUrl des ', previusUrl);
      })
   }
}, [requestedUrl]);

   return (
      <Fragment>
            <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>
         <div className="row d-flex justify-content-center mb-3 pb-3">
               <Link to={'history-abc'} className="text-light col-3">
                  <div className="btn btn-success" >
                        Historique Abonnements
                  </div>
               </Link> 
               <Link to={'history-trans'} className="text-light col-3">
                  <div className="btn btn-danger" >
                     Historique Transactions
                  </div>
               </Link> 
               <Link to={'history-presence'} className="text-light col-3">
                  <div className="btn btn-info" >
                     Historique Presences
                  </div>
               </Link> 
               {/* <Link to={'history-transactions'} className="text-light">
            <div className="btn btn-info col-3" >
                  Historique Transactions
            </div>
                  </Link> 
               <Link to={'history-presence'}className="text-light">
            <div className="btn btn-info col-3" >
            Historique Presences
            </div>
               </Link> */}
         </div>
         <div className="row d-flex m-3 py-4" style={{backgroundColor:'#ffffff'}}>
            <div className=" col-md-2">
               <label style={{color:'#000000'}} >Adhérant </label>
               <input type="text" className="form-control" placeholder="rechercher par ID Client" value={searchValue} onChange={e => setSearchValue(e.target.value)}/>
            </div>
            <div className=" col-md-2">
               <label style={{color:'#000000'}} >Abonnement ID </label>
               <input type="text" className="form-control" placeholder="rechercher par ID Abonnement" value={abcId} onChange={e => setAbcId(e.target.value)}/>
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} >Utilisateur</label>
                  <Autocomplete
                  // id={(option) =>  option['id']}
               
                  // onChange={handleSubmit}
                  options={users}
                  onChange={((event, value) =>  {
                     try {
                        setUserId(value.id)
                     } catch (error) {
                        setUserId('')
                     }
                  })}
                  //  value={activities[creneauActivite]}
                  getOptionSelected={(option) =>  option['id']}
                  getOptionLabel={(option) =>  option['email']}
                  style={{ color: '#000' }}
                  renderInput={(params) => 
                     <TextField {...params} style={{color:"#000"}}  className='text-light' label="Utilisateur" variant="outlined"  
                     InputLabelProps={{style: { color: '#000', borderColor:'#000' }, }}
                     />}
                  />
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="birth_date">Date début </label>
               <input type="date" name="start_date" className="form-control" value={startDate}  onChange={e => setStartDate(e.target.value)}/>
            </div>
            <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="end_date">Date Fin </label>
               <input type="date" name="end_date" className="form-control" value={endDate} onChange={e => setEndDate(e.target.value)}/>
            </div>
            {/* <div className="form-group col-md-2">
               <label style={{color:'#000000'}} htmlFor="start_hour">Heure du créneau</label>
               <input type="time" name="start_hour" className="form-control" value={startHour} onChange={e => setStartHour(e.target.value)}/>
            </div> */}
         </div>
         <div className="row">
            <div className="col-lg-12">
               <div className="card">
                  <div className="card-body" style={{padding: '5px'}}>
                     <div className="table-responsive">
                        <table className="table mb-0 table-striped">
                           <thead>
                              <tr>
                                 <th className="customer_shop"> Abonnement ID </th>
                                 <th> Adhérant</th>
                                 <th> Date de création </th>
                                 <th> Date de changement </th>
                                 <th className="pl-5 width200">Séances </th>
                                 <th> Notes </th>
                                 <th className='text-right'>Dettes </th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                              {abcsData.map(abc => (
                                 <tr role="row presences" key={abc.history_id} className="btn-reveal-trigger cursor-abonnement presences p-0">
                                    <td className="customer_shop_single"> {abc.id} </td>
                                    <td className="customer_shop_single"> {abc.client} </td>
                                    <td >{abc.created_date_time}</td>
                                    <td >{abc.history_date}</td>
                                    <td >{abc.is_time_volume ? abc.left_minutes : abc.is_free_access ? 'Forfait': abc.presence_quantity }</td>
                                    <td className=" text-left">{abc.history_user_name}</td>
                                    <td className=" text-right text-danger">{abc.reste}</td>
                                 </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
            {/* <PresenceEditModal show={editModal} onShowShange={setEditModal} presenceData={{presenceId:presenceId, client:client, hourIn:hourIn, hourOut: hourOut, creneau:creneau, note:note, clientId:clientId, date:date, activity:activity}}/>
            <PresenceCreateModal show={presneceCreateModal} onShowShange={setPresneceCreateModal} /> */}
         </div>
         <div className='d-flex text-center justify-content-end'>
               <div className='dataTables_paginate paging_simple_numbers' id='example5_paginate' >
                  {
                     previusUrl && 
                     <Button
                        onClick={() => {
                           if( nextpage > 1 ) {
                              setRequestedUrl(previusUrl)
                              nextpage > 0 && setNextpage(nextpage - 1)
                           }
                        }}
                        style={{ width: '100px', border: 'none', height: '48px', color: '#ffffff', textAlign: 'left', fontSize: '15px', paddingLeft: '8px' }}>
                        Précédent
                     </Button>
                  }
                  {
                     previusUrl ? <span className="m-3" >{nextpage}</span> : nextUrl ?  <span className="m-3" >{nextpage}</span> : ""
                  }
                  {
                     nextUrl && 
                     <Button
                        style={{ width: '100px', border: 'none', height: '48px', color: '#ffffff', textAlign: 'center', fontSize: '15px', padding: '2px' }}
                        onClick={() => {
                           setRequestedUrl(nextUrl)
                           nextpage > 0 && setNextpage(nextpage + 1)
                        }}
                     >
                        Suivant
                     </Button>
                  }
               </div>
            </div>
      </Fragment>
   );
};

export default HistoryTrans;
