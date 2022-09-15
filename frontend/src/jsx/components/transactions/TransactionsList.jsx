import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import Search from "../../layouts/Search";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
import PaiementCreateModal from './PaiementCreateModal';
import RemunerationCoachModal from './RemunerationCoachModal';
import RemunerationPersonnelModal from './RemunerationPersonnelModal';
import useAxios from "../useAxios";
import AutreCreateModal from './AutreCreateModal';
// import DetteCreateModal from './DetteCreateModal';
/// images 


import { Link, useHistory } from "react-router-dom";
import { transformToNestObject } from "react-hook-form";

import {
   MuiPickersUtilsProvider,KeyboardDatePicker
 } from '@material-ui/pickers';
 import DateFnsUtils from '@date-io/date-fns';
import useAuth from "../useAuth";
 


const TransactionList = () => {
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
   
const [startDate, setStartDate] = useState(formatDate(new Date('2021-01-05')));
   const [endDate, setEndDate] = useState(formatDate(new Date()));
   const [paiementModal, setPaiementModal] = useState(false);
   const [autreModal, setAutreModal] = useState(false);
   const [remunerationCoachModal, setRemunerationCoachModal] = useState(false);
   const [remunerationPersonnelModal, setRemunerationPersonnelModal] = useState(false);
   const [detteModal, setDetteModal] = useState(false);
   // const [modal, setModal] = useState(false);
   const [presenceData, setPresenceData] = useState([]);
   const [searchValue, setSearchValue] = useState('')
   const [transData, setTransData] = useState([]);
   // const savedTransactions = (endpoint)
   // console.log('els clieeents', savedTransactions);
   const capitalizeFirstLetter = (word) => {
      if (word)
          return word.charAt(0).toUpperCase() + word.slice(1);
      return '';
   };

   // useEffect(() =>  {
   //    const dateDebut = formatDate(startDate)
   //    const dateFin = formatDate(endDate)
   //    if (searchValue !== '') {
   //       api.get(`${process.env.REACT_APP_API_URL}/rest-api/transactions/?start_date=${dateDebut}&end_date=${dateFin}&search=${searchValue}`).then(res => {
   //          setTransData(res.data)
   //          console.log('le resultat des clients est ', res.data);
   //       })
   //    }else {

   //       api.get(`${process.env.REACT_APP_API_URL}/rest-api/transactions/?start_date=${dateDebut}&end_date=${dateFin}&search=${searchValue}`).then(res => {
   //          setTransData(res.data)
   //          console.log('le resultat des clients est ', res.data);
   //       })}
   // }, [searchValue]);

   const [uStatus, setUStatus] = useState(null);

   const [nextpage, setNextpage] = useState(1);

   const history = useHistory();

   const dateDebut = formatDate(startDate)
   const dateFin = formatDate(endDate)
   
   const transactionAuth = `${process.env.REACT_APP_API_URL}/rest-api/transactions/?page=${nextpage}&start_date=${dateDebut}&end_date=${dateFin}`;

   useEffect(() =>  {
      // api.get(`${process.env.REACT_APP_API_URL}/rest-api/presence/?start_date=${startDate}&end_date=${endDate}`).then(res => {
      //    setStartDate(res.data.results)
      //    setEndDate(res.data.results)
      //    console.log('le resultat des clients est ', res.data);
      // })

    

      api.get(transactionAuth).then( res => {
         // setUStatus(res.status);
         console.log(res.status);
         console.log('result ', res);
         setUStatus(res.status);

         // setTransData(res.data.results);
         // console.log(res.status)
         // return res.status < 400;
      }).catch((error) => {
         if (error.response) {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            setUStatus(error.response.status);


      }
   })

   
   // !!! rahi : if clientAuth == true , il n'affiche pas la listes des client car la listes des client endpoint is diffrent -- clientList.jsx
   // f admin meme ki ndir permissions,  f Network y'affichili bli i dont have access ( error 403 )

   

   // api.get(`${process.env.REACT_APP_API_URL}/rest-api/clients-name-drop/`).then(res => {
   //    console.log(res.status);
   //    setUStatus(res.status);
   // }).catch(error => {
   //    if (error.response) {
   //       console.log(error.response.data);
   //       console.log(error.response.status);
   //       console.log(error.response.headers);
   //       setUStatus(error.response.status);
   //    }
   // })

      // const presenceDateDate =  () => {
         // const page = nextpage
      // }
   // }else {
   //    api.get(endpoint).then(res => {
   //       setStartDate(res.data.results)
   //       setEndDate(res.data.results)
   //       console.log('le resultat des clients est ', res.data);
   //    })}
   // presenceDateDate()
   }, [startDate, endDate,nextpage,paiementModal,remunerationCoachModal,remunerationPersonnelModal,autreModal]);


   const trAuth = useAuth(transactionAuth, 'GET')


   console.log("trAuth ===> ", trAuth);

   return (
      <Fragment>
        
         <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts  />
         </div>
         {trAuth && (
         <>

            {/* <Search name= 'Abonnée' lien= "/client/create"/> */}
            <div className="row d-flex justify-content-arround mb-3">
                  <div className="btn btn-success ml-auto" onClick={e => setPaiementModal(true) }>
                     + Paiement 
                  </div>
                  <div className="btn btn-danger ml-auto" onClick={e => setRemunerationPersonnelModal(true) }>
                  + Remunération Personnel 
                  </div>
                  <div className="btn btn-info ml-auto" onClick={e => setRemunerationCoachModal(true) }>
                  + Remunération Coach
                  </div>
                  <div className="btn btn-primary ml-auto" onClick={e => setAutreModal(true) }>
                  + Autre Transaction
                  </div>
                <div className="col-md-2">
                      <input type="date"  value={startDate} className="form-control"  onChange={e => setStartDate(e.target.value)}/>
               </div>
               <div className=" col-md-2">
                     <input type="date"  value={endDate} className="form-control"  onChange={e => setEndDate(e.target.value)}/>
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
                                 {/* <th className="customer_shop"> ID </th> */}
                                 <th>Date</th>
                                 <th>montant</th>
                                 <th>Type</th>
                                 <th className="pl-5 width200"> Nom </th>
                                 <th className="pl-5 width200">Note</th>
                                 <th></th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                           {transData.map(tran => (
                              <tr role="row" key={tran.id} className="btn-reveal-trigger presences">
                                 <td className="customer_shop_single">
                                       <div className="media d-flex align-items-center">
                                          <div className="media-body">
                                             <h5 className="mb-0 fs--1">
                                             {capitalizeFirstLetter(tran.date_creation)}
                                             </h5>
                                          </div>
                                       </div>
                                 </td>
                                 <td className="">
                                    <h5 style={ tran.type === 'remunerationProf' || tran.type === 'remuneration'  ? {color: '#FF2E2E'} : tran.type === 'paiement' || tran.type === 'assurance' ? {color: '#24a247'} :  {color: '#000000'}  }>{tran.amount}</h5>
                                 </td>
                                 <td className="">
                                  {tran.type === 'remunerationProf' ? 'Coach' : tran.type === 'paiement' ? capitalizeFirstLetter(tran.abonnement_name) : tran.type === 'remuneration'  ? 'Personnel' : tran.type === 'assurance' ? 'Frais Annuel' : 'Autre'} 
                                 </td>
                                     { tran.coach &&
                                       <td className=" ">
                                          <Link to={`/coach/${tran.coach.id}`} >
                                             {tran.coach.name} 
                                          </Link> 
                                       </td>
                                     }
                                     {tran.abonnement_client && 
                                       <td className=" "> 
                                          <Link to={`/client/${tran.client_id}`} >
                                             {tran.client_last_name}  
                                          </Link> 
                                       </td>
                                     }
                                       {tran.type === 'remuneration' &&
                                             <td className=" "> 
                                             {tran.client.name}
                                             </td>
                                       }
                                       {tran.type === 'autre' &&
                                             <td className=" "> 
                                             {tran.name}
                                             </td>
                                       }
                                       {tran.type === 'assurance' &&
                                             <td className=" "> 
                                             {tran.name}
                                             </td>
                                       }
                                 <td className=" pl-5"> { tran.notes } </td>
                                 {/* <td className="">30/03/2018</td> */}
                                 {/* <td className=" text-right">
                                    <Drop id={tran.id}/>
                                 </td> */}
                              </tr>
                              ))}
                           </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
            {/* <TransactionCreateModal show={modal} onShowShange={setModal}/> */}
            <PaiementCreateModal show={paiementModal} onShowShange={setPaiementModal}/>
            <RemunerationCoachModal show={remunerationCoachModal} onShowShange={setRemunerationCoachModal}/>
            <RemunerationPersonnelModal show={remunerationPersonnelModal} onShowShange={setRemunerationPersonnelModal}/>
            <AutreCreateModal show={autreModal} onShowShange={setAutreModal}/>
         </div>
         <div className='d-flex text-center justify-content-end'>
            <div className='dataTables_info text-black' id='example5_info '>
          
            </div>
            <div className='dataTables_paginate paging_simple_numbers' id='example5_paginate' >
            <Button
               onClick={() =>
               nextpage > 0 && setNextpage(nextpage - 1)
            }
            style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'left', fontSize:'15px', paddingLeft:'8px'}}>
               Précédent
            </Button>
            <span>
                  <input
                  to='/transactions'
                  type='number'
                  className='paginate_button_client  '
                  onChange={e => setNextpage(e.target.value)}
                  value={nextpage}
                  style={{width: '100px', border: 'none', height:'99%', textAlign: 'center', fontSize:'15px'}}
                  />
            </span>
            <Button
            style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'center', fontSize:'15px', padding:'2px'}}
            onClick={() =>
               nextpage > 0 && setNextpage(nextpage + 1)
            }
            >
               Suivant
            </Button>
            </div>

         </div>
   
         </>  
         )}

      </Fragment>
   );
};

export default TransactionList;
