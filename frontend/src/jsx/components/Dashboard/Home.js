import React, { Fragment , useState, useEffect} from "react";
import { Dropdown, Tab, Nav, Row } from "react-bootstrap";
import { Link, Router, useHistory } from "react-router-dom";
import { useGetAPI, usePutAPI } from '../useAPI'

import PerfectScrollbar from "react-perfect-scrollbar";

// import Contacts from "../Dhrev/Home/slider/Contacts";
import ShortCuts from "../ShortCuts";
import axios from "axios";

const Home = () => {

  //  const dettesAND = `${process.env.REACT_APP_API_URL}/rest-api/clients-dettes/`
   const dettesAND = `${process.env.REACT_APP_API_URL}/rest-api/totales-restes/`
   const chargesAND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/total-charges/`
   const ttcAND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/chiffre-affaire/`
   const clientCount = `${process.env.REACT_APP_API_URL}/rest-api/clients-count/`
   const transactionsTodayEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/trans-today/`
   const presencesTodayEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/is-in/`
   let presenceCreateEND =  `${process.env.REACT_APP_API_URL}/rest-api/presence/create`
   // let coachsEND = `${process.env.REACT_APP_API_URL}/rest-api/coachs/`
   let presencesParSalleEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/by-salles/`
  
   const [client, setClient ] = useState('')
   const [presenceId, setPresenceId ] = useState('')
  
   const [coachData, setCoachData] = useState([]);
   
   
   const [ chiffreDaffaire, setChiffreDaffaire]= useState('')
  
   const [ dettesglobal, setDettesglobal]= useState('')
   const [ nombreAbonne, setNombreAbonne]= useState(253)
   const [ totaldepenses, setTotaldepenses]= useState('')
   const [transClient, setTransClient] = useState([]);
   const [abonClient, setAbonClient] = useState([]);
   const [abonDetailModal, setAbonDetailModal] = useState(false);
   const [abonClientType, setAbonClientType] = useState("");
   const [abonClientID, setAbonClientID] = useState("");
   const [abonClientEnd, setAbonClientEnd] = useState("");
   const [abonClientpresences, setAbonClientpresences] = useState("");
   const [presencesClient, setPresnecesClient] = useState([]);
   const [salle, setSalle] = useState([]);
   // const dettes = useGetAPI(dettesAND)
   // setDettesglobal(dettes)
   // console.log('dettesglobal', dettes);
   
   useEffect(() => {
      axios.get(dettesAND).then((res) => {
         setDettesglobal(res.data['totales_dettes']['reste__sum'])
      })
      axios.get(chargesAND).then((res) => {
         setTotaldepenses(res.data.total_charges)
      })
      axios.get(ttcAND).then((res) => {
         setChiffreDaffaire(res.data.chiffre_affaire)
      })
      axios.get(clientCount).then((res) => {
         setNombreAbonne(res.data.abonnees)
      })
      axios.get(transactionsTodayEND).then((res) => {
         setTransClient(res.data)
         console.log('res trans clients', res.data);
      })
      axios.get(presencesTodayEND).then((res) => {
         setPresnecesClient(res.data)
         console.log('les clients actuellement en salle', res.data);
      })
      // axios.get(coachsEND).then((res) => {
      //    setCoachData(res.data)
      // })
   }, []);
   useEffect(() => {
      axios.get(presencesParSalleEnd).then( res => {
         setSalle(res.data.presences)
         console.log('presenEEEESSSSS', res.data);
      })
   }, []);
   let history = useHistory()
   const ToFicheClient = (clientID) => {
      history.push(`/client/${clientID}`)
   }
   const HandlePresenceSubmit = (e) => {
      e.preventDefault();
      const clientId = {client : Number(client)}
      // getIdPresence(client)
      axios.get(`${process.env.REACT_APP_API_URL}/rest-api/clients/${client}/`).then(res=> {
         if (res.data.last_presence) {
            
            console.log('id de la presence', res.data.last_presence);
            setPresenceId(res.data.last_presence)
            console.log('erreur lors du cposr ligne 85', presenceId);
            axios.patch( `${process.env.REACT_APP_API_URL}/rest-api/presence/edit/${res.data.last_presence}/`)
         }else {

            axios.post(presenceCreateEND, clientId)
         }
      }).catch( err => {

         console.log('erreur lors du cposr',err);
      }

   )}
   return (
      <Fragment>
         <>
            <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
              <ShortCuts />
            </div>
      <div className="row">
        <div className="col-xl-3 col-xxl-6 col-lg-6 col-sm-6 ">
          <div className="card currency-bx overflow-hidden relative bg-warning">
            <div className="card-body p-4">
              <div className="media align-items-center">
                <div className="media-body">
                  <h5 className="text-white fs-20">Chiffre D'affaire Global</h5>
                  <h1 className="text-white mb-0">{chiffreDaffaire}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-xl-3 col-xxl-6 col-lg-6 col-sm-6 ">
          <div className="card currency-bx overflow-hidden relative bg-secondary">
            <div className="card-body p-4">
              <div className="media align-items-center">
                <div className="media-body">
                  <h5 className="text-white fs-20">Total Dépenses</h5>
                  <h1 className="text-white mb-0">{totaldepenses}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-xl-3 col-xxl-6 col-lg-6 col-sm-6 ">
          <div className="card currency-bx overflow-hidden relative bg-info">
            <div className="card-body p-4">
              <div className="media align-items-center">
                <div className="media-body">
                  <h5 className="text-white fs-20">Total Dettes</h5>
                  <h1 className="text-white mb-0">{dettesglobal}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-xl-3 col-xxl-6 col-lg-6 col-sm-6 ">
          <div className="card currency-bx overflow-hidden relative bg-dark">
            <div className="card-body p-4">
              <div className="media align-items-center">
                <div className="media-body">
                  <h5 className="text-white fs-20">Total Adherants</h5>
                  <h1 className="text-white mb-0">{nombreAbonne}</h1>
                </div>
              </div>
            </div>
            {/* <img className="bg-img" src={turkish} alt="" /> */}
          </div>
        </div>
      </div>
        <div className="row">
         <div className="col-lg-4 col-xxl-4  col-sm-6">
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Transactions du jour   </h4>
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar
                style={{ height: "370px" }}
                id="DZ_W_TimeLine"
                className="widget-timeline dz-scroll height370 ps ps--active-y"
                >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th className="text-left"><h5>Mantant</h5></th>
                      <th><h5>type</h5></th>
                      <th><h5>nom</h5></th>
                    </tr>
                  </thead>
                  <tbody>
                    {transClient.map(tran => (
                      <tr key={tran.id}>
                      <td className="text-left"><h5 style={
                                       tran.type === 'remunerationProf' || tran.type === 'remuneration'  ? {color: '#FF2E2E'} : tran.type === 'paiement' || tran.type === 'assurance' ? {color: '#24a247'} :  {color: '#000000'}}>{tran.amount}</h5></td>
                      {/* <td>0.18</td> */}
                      <td className="py-2">
                        {tran.type === 'remunerationProf' ? 'Rémuneration Coach' : tran.type} 
                     </td>
                           { tran.coach &&
                           <td className="py-2 pl-5 wspace-no">
                              <Link to={`/coach/${tran.coach.id}`} >
                                 {tran.coach.name} 
                              </Link> 
                           </td>
                           }

                           {tran.client && 
                           <td className="py-2 pl-5 wspace-no"> 
                              <Link to={`/client/${tran.client.id}`} >
                                 {tran.client.name}  
                              </Link> 
                           </td>
                           }
                           {tran.client_last_name && 
                           <td className="py-2 pl-5 wspace-no"> 
                              <Link to={`/client/${tran.client_id}`} >
                                 {tran.client_last_name} - {tran.client_id}  
                              </Link> 
                           </td>
                           }
                           {tran.type === 'autre' &&
                              <td className="py-2 pl-5 wspace-no"> 
                              --
                              </td>
                           }
                    </tr>
                    ))
                    }
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>

            </div>
            <div className="card-footer border-0 pt-0 text-center">
              <Link to="/transactions" className="btn-link">
                Transactions <i className="fa fa-caret-right ml-2 scale-2" />
              </Link>
            </div>
          </div>
        </div>
        {/* .........................   Fin trasantions........................ */}
        
        {/* .........................   Fin Abonnements........................ */}
         {/* .........................   les Presences........................ */}
         <div className="col-lg-4 col-xxl-4  col-sm-6" >
          <div className="card" >
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Présences par salle</h4>
               {/* <form onSubmit={HandlePresenceSubmit}>
              <input type="text" className="form-control" placeholder="ID client" onChange={e => { 
                  setClient(e.target.value)
                  }} />
               </form> */}
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar
                style={{ height: "370px" }}
                id="DZ_W_TimeLine"
                className="widget-timeline dz-scroll height370 ps ps--active-y"
              >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>

                    <tr >
                      <th  className="text-left">Salle</th>
                      <th className="text-right">Présences</th>
                    </tr>
                  { salle.map ( presence => (
                    <tr  key={presence.name}>
                      {/* <td>{presence.name}</td> */}
                      <td className="text-left">{presence.name}</td>
                      <td className="text-right">{presence.actvities__creneaux__presenses__count}</td>
                  
                    </tr>
                    ))}
                  </thead>
                  <tbody>
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>
            </div>
            <div className="card-footer border-0 pt-0 text-center">
              <Link to="/presences" className="btn-link">
                Presences <i className="fa fa-caret-right ml-2 scale-2" />
              </Link>
            </div>
          </div>
        </div>
        <div className="col-lg-4 col-xxl-4 col-sm-6" >
          <div className="card" >
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Actuellement en salle</h4>
               {/* <form onSubmit={HandlePresenceSubmit}>
              <input type="text" className="form-control" placeholder="ID client" onChange={e => { 
                  setClient(e.target.value)
                  }} />
               </form> */}
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar
                style={{ height: "370px" }}
                id="DZ_W_TimeLine"
                className="widget-timeline dz-scroll height370 ps ps--active-y"
               >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr >
                      <th className="text-left">ID</th>
                      <th >Nom</th>
                      <th >Activité</th>
                      <th >Dettes</th>
                      {/* <th className="text-right">Salle</th> */}
                    </tr>
                  { presencesClient.map ( presence => (
                    <tr className='ajouter' key={presence.id} onClick={ e => ToFicheClient(presence.client)}>
                      {/* <td>{presence.name}</td> */}
                      {/* <td>{presence.hour_sortie}</td> */}
                      <td className="text-left">{presence.client}</td>
                      <td >{presence.client_last_name}</td>
                      <td >{presence.client_activity}</td>
                      
                                      
                      
                      <td style={presence.dettes > 0 ? {color: '#FF2E2E'} : {color: '#000000'}}>{presence.dettes}</td>
                    </tr>
                    ))}
                  </thead>
                  <tbody>
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>
            </div>
            <div className="card-footer border-0 pt-0 text-center">
              <Link to="/presences" className="btn-link">
                Presences <i className="fa fa-caret-right ml-2 scale-2" />
              </Link>
            </div>
          </div>
        </div>
        {/* <div className="col-xl-6 col-xxl-12 col-lg-12">
                  <div className="card">
                     <div className="card-header d-sm-flex d-block pb-0 border-0">
                        <div>
                           <h4 className="text-black fs-20">Chiffre d'affaire</h4>
                           <p className="fs-13 mb-0">
                              Etat de chiffre d'affaire par mois 
                           </p>
                        </div>
                        <Dropdown className="mt-sm-0 mt-3">
                           <Dropdown.Toggle variant="" className="btn rounded-0 text-black bgl-light dropdown-toggle " >
                              Monthly (2021)
                           </Dropdown.Toggle>
                           <Dropdown.Menu
                              align="right"
                              className="dropdown-menu dropdown-menu-right"
                           >
                              <Link className="dropdown-item" to="/">
                              Monthly (2020)
                              </Link>
                              <Link className="dropdown-item" to="/">
                              Monthly (2019)
                              </Link>
                              <Link className="dropdown-item" to="/">
                              Monthly (2018)
                              </Link>
                           </Dropdown.Menu>
                        </Dropdown>
                     </div>
                     <div className="card-body" id="user-activity">
                        <Tab.Container defaultActiveKey="all">
                           <div className="d-flex flex-wrap justify-content-between mb-5">
                              <div className="card-action card-tabs icontabs mt-3 mt-sm-0">
                                 
                              </div>
                              <div className="d-flex align-items-center mt-3 mt-sm-0">
                                 <p className="mb-0 fs-13 mr-3">Dernier Mois</p>
                                 <h2 className="mb-0 text-black font-w600">
                                    {chiffreDaffaire}
                                 </h2>
                              </div>
                           </div>
                           <Tab.Content
                              className="tab-content"
                              id="myTabContent"
                           >
                              <Tab.Pane eventKey="all">
                                 <ActivityLine />
                              </Tab.Pane>
                              <Tab.Pane eventKey="btc">
                                 <ActivityLine2 />
                              </Tab.Pane>
                              <Tab.Pane eventKey="ethereum">
                                 <ActivityLine3 />
                              </Tab.Pane>
                           </Tab.Content>
                        </Tab.Container>
                     </div>
                  </div>
               </div>
            */}
            </div> 
         </>
      </Fragment>
   );
};

export default Home;
