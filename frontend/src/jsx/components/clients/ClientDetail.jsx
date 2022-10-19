import React, { useState , useEffect, useRef} from "react";
import { Link } from "react-router-dom";
// import productData from "../productData";
import { ToastContainer } from 'react-toastify'
import {notifySuccess, notifyError} from '../Alert'

import { Helmet } from 'react-helmet'
import { Dropdown, Tab, Nav, Button } from "react-bootstrap";
import {
  Row,
  Col,
  Card,
  Table,
  Badge,
  ProgressBar,
} from "react-bootstrap"

import PerfectScrollbar from "react-perfect-scrollbar";
import product1 from "../../../images/product/1.jpg";
import Search from "../../layouts/Search";
import { createContext } from "react";
import ABCCreateModal from './ABCCreateModal';
import PaiementModal from './PaiementModal'
import ABCDetailModal from './ABCDetailModal'
import ShortCuts from "../ShortCuts";
import AssuranceCreateModal from './AssuranceCreateModal';
import PaiementsClientModal from './PaiementsClientModal';
import PresencesClientModal from './PresencesClientModal';
import PaiementEditModal from './PaiementEditModal';
import RenewAbonnementModal from './RenewAbonnementModal';
import AbonnementClientModal from './AbonnementClientModal';
import femaleImg from "../../../images/profile/female.png";
import useAxios from "../useAxios";
import ReactToPrint from 'react-to-print';
import { ComponentToPrint } from './ComponentToPrint';

const ComponentToPrintWrapper = ({ item }) => {
  //console.log('iteMM', item);
  const componentRef = useRef();

  const marginTop="40px"
  const marginRight="5px"
  const marginBottom="40px"
  const marginLeft="5px"


  const getPageMargins = () => {
    return `@page { margin: ${marginTop} ${marginRight} ${marginBottom} ${marginLeft}  !important; }`;
  };

// const pageStyle = `
//   @page {
//     size: landscape;
//   }
// `;

  return (
    <div style={{ display: "flex"}}>
     
      <ReactToPrint
        trigger={() =>   <div > Imprimer <i className="fa la-print text-danger mr-2 h5" /> </div>}
        content={() => componentRef.current }
    
      />
      <div className="d-none">
        <style> {getPageMargins()}</style>
        <ComponentToPrint ref={componentRef} value={item}></ComponentToPrint>
      </div>
    </div>
  );
};


const ProductDetail = (props) => {
  const [client, setClient] = useState({});
  const [aBCmodalCreate, setABCModalCreate] = useState(false);
  const [paiementModal, setPaiementModal] = useState(false);
  const [abonDetailModal, setAbonDetailModal] = useState(false);
  const [abonClient, setAbonClient] = useState([]);
  const [transClient, setTransClient] = useState([]);
   const [presencesClient, setPresnecesClient] = useState([]);
   const [dettesClient, setDettesClient] = useState([]);
   const [creneauxClient, setCreneauxClient] = useState([]);
   const [abonClientID, setAbonClientID] = useState("");
   const [abonClientType, setAbonClientType] = useState("");
   const [presenceSuccess, setPresenceSuccess] = useState(false);
   const [presenceError, setPresenceError] = useState(false);
   const [abonClientTypeName, setAbonClientTypeName] = useState("");
   const [paiementAmountInfo, setPaiementAmountInfo] = useState("");
   const [paiementABCInfo, setPaiementABCInfo] = useState("");
   const [paiementABCName, setPaiementABCName] = useState("");
   const [paiementDateInfo, setPaiementDateInfo] = useState("");
   const [paiementEditModal, setPaiementEditModal] = useState(false);
   const [paiementIdInfo, setPaiementIdInfo] = useState("");
   
   
   const [abonClientEnd, setAbonClientEnd] = useState("");
   const [abonClientpresences, setAbonClientpresences] = useState("");
   const [paiementNotesInfo, setPaiementNotesInfo] = useState("");
   const [abonClientReste, setAbonClientReste] = useState("");
   const [abonnementClientCreneaux, setAbonnementClientCreneaux] = useState([]);
   const [assuranceModal, setAssuranceModal] = useState(false);
   const [clientPaiementsModal, setClientPaiementsModal] = useState(false);
   const [clientPresencesModal, setClientPresencesModal] = useState(false);
   const [clientAbcModal, setClientAbcModal] = useState(false);
   const [renewAbcModal, setRenewAbcModal] = useState(false);
   
   const clientId = props.match.params.id;
   const presenceCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/create`
   const transactionClientEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement-by-client/?cl=${clientId}`
  const creneauClientEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-client?cl=${clientId}`
  // //console.log('les trnasactions ',transactions);
  // //console.log('le id de labonnd client est ', abonnementClientCreneaux);
  const api = useAxios();

  const addPresence = async () => {
    const clientData =  {
      client : Number(clientId)
    }
    try {
      const axWait = await api.post(presenceCreateEND, clientData)
      notifySuccess('Presence enregistré avec succés')
        return axWait
    } catch (error) {
      notifyError("Cet adherant n'a aucun cours maintenant")
      }
    }
  // useEffect(() => {
  //   if (presenceSuccess == true) {
  //     notifyPresenceSuccess()
  //   }
  // }, [presenceSuccess]);
  // useEffect(() => {
  //   if (presenceError == true) {
  //     notifyPresenceError()
  //   }
  // }, [presenceError]);

  // const notifyPresenceSuccess = () => {
  //   toast.success('Activité Creer Avec Succée', {
  //     position: 'top-right',
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //   })
  // }
  // const notifyPresenceError = () => {
  //   toast.error('le client avec l\'ID ' +' ' + clientId +' ' +"n'a pas le droit d'assisté a cours", {
  //     position: 'top-right',
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //   })
  // }

  // useEffect(() => {
  //   //  const clientId = props.match.params.id;
  //    const fetchData = async () => {
  //       try {
  //          const res = await api.get(creneauClientEND);
  //          let creneaux = res.data
  //         //  let result = (creneaux) => creneaux.filter((v,i) => creneaux.indexOf(v) === i)
  //          setCreneauxClient(creneaux)
 
  //           // //console.log('ghirrrr =creneauxClient', creneauxClient);
  //       } catch (error) {
  //          console.log(error, 'erreur presneces');
  //       }
  //    }
  //    fetchData();
  // }, [props.match.params.id] );
  useEffect(() => {
     const fetchData = async () => {
        try {
           const res = await api.get(`${process.env.REACT_APP_API_URL}/rest-api/clients/${clientId}/`);
           setClient(res.data);
        } catch (error) {
           console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id] );

  useEffect(() => {
     const fetchData = async () => {
        try {
           const res = await api.get(creneauClientEND);
           setCreneauxClient(res.data)
        } catch (error) {
          console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id, aBCmodalCreate, abonDetailModal] );
  
  useEffect(() => {
     const fetchData = async () => {
        try {
           const res = await api.get(transactionClientEND);
           setTransClient(res.data)
           const res2 = await api.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement-client-dettes/?cl=${clientId}`);
           setDettesClient(res2.data.abonnees.reste__sum)
        } catch (error) {
           console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id,  aBCmodalCreate, , paiementModal, paiementEditModal,abonDetailModal] );
  useEffect(() => {
    //  const clientId = props.match.params.id;
     const fetchData = async () => {
        try {
           const res = await api.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client/?cl=${clientId}`);
           setAbonClient(res.data)
        } catch (error) {
           console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id, aBCmodalCreate, abonDetailModal, paiementModal, paiementEditModal] );

const capitalizeFirstLetter = (word) => {
   if (word)
       return word.charAt(0).toUpperCase() + word.slice(1);
   return '';
};

const populatePaimentData = (e) => {
  setPaiementIdInfo(e.target.id)
  setPaiementAmountInfo(e.target.amount)
  setPaiementABCInfo(e.target.abonnement_name)
  setPaiementDateInfo(e.target.date_creation)
  setPaiementEditModal(true)
  //console.log('TRHE RRRREEEE', e.target);
}
useEffect(() => {
  try {
    populatePaimentData()
  } catch (error) {
    
  }
}, [populatePaimentData]);
  return (
    <>
     <Helmet>
          <title>{String(clientId)} - {String(client.last_name)} </title>
        </Helmet>
      <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
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
      {/* info profile */}
      <div className="profile-info">
        <div className="profile-photo">
            <img src={client.picture  ? `${process.env.REACT_APP_API_URL}${client.picture}` : femaleImg} className="img-fluid rounded-circle" alt="profile" width='90' />
        </div>
        <div className="profile-details">
          <div>
            <div className="profile-name px-3 pt-2">
              <h4 className="text-primary mb-0">
              {capitalizeFirstLetter(client.last_name)} {capitalizeFirstLetter(client.first_name)}
              </h4>
              <p>ID: <span className='text-danger'>{client.id}</span></p>
            </div>
            <div className="social-icons">
                <Link to={`/client/edit/${client.id}`} className="btn-xs btn-primary light" > Modifier Profile </Link>
            </div>
          </div>
            <div className="profile-email px-2 pt-2">
              <h4 className="text-muted mb-0">
              inscrit le : {client.date_added}
              </h4>
              {
                client.debut_assurance !== 'false'
                &&
                <h5 className='mt-3'>Début frais Annuel: <span style={new Date() > new Date(client.fin_assurance) ? {color: 'red'} : {color: '#06eeee'} }>{client.debut_assurance} </span></h5>
              }
              <p>Fin Frais Annuel : <span style={new Date() > new Date(client.fin_assurance) ? {color: 'red'} : {color: '#06eeee'} }>{client.fin_assurance}   {new Date() > new Date(client.fin_assurance) && 'éxpiré' } </span>
              {new Date() > new Date(client.fin_assurance) && <Button className="btn-xs  btn-danger light m-3 ml-auto" onClick={e => setAssuranceModal(true) }>Payer</Button> }</p>
            </div>
            <div className="profile-email px-2 pt-2">
              <h4 className="text-muted mb-0">
                {client.note}             
              </h4>
            </div>
            <div className="profile-email text-danger pt-2" style={{marginLeft: 'auto'}}>
              <h3 className="text-danger mb-0">
                Dettes :{dettesClient}             
              </h3>
            </div>
            <Dropdown className="dropdown ml-auto">
              <Dropdown.Toggle  variant="primary"  className="btn btn-primary light sharp i-false"  data-toggle="dropdown"  aria-expanded="true" >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" viewBox="0 0 24 24" version="1.1" >
                    <g  stroke="none"  strokeWidth="1"  fill="none"  fillRule="evenodd" >
                      <rect x="0" y="0" width="24" height="24" ></rect>
                      <circle fill="#000000" cx="5" cy="12" r="2" ></circle>
                      <circle fill="#000000" cx="12" cy="12" r="2" ></circle>
                      <circle  fill="#000000"  cx="19"  cy="12"  r="2" ></circle>
                    </g>
                  </svg>
              </Dropdown.Toggle>
              <Dropdown.Menu className="dropdown-menu dropdown-menu-right">
                  <Dropdown.Item className="dropdown-item" href= {`/client/edit/${client.id}`}>
                    <i className="fa fa-user-circle text-primary mr-2" />
                    Modifier profile
                  </Dropdown.Item>
                  <Dropdown.Item className="dropdown-item" onClick= { e => addPresence(true)}>
                    
                  <i className="fa fa-plus text-primary mr-2" />
                    Ajouter Presence
                  </Dropdown.Item>
                  
                  <Dropdown.Item className="dropdown-item" onClick= { e => setABCModalCreate(true)}>
                    <i className="fa fa-plus text-primary mr-2" />
                    Ajouter Abonnement 
                  </Dropdown.Item>

                  <Dropdown.Item className="dropdown-item" onClick= { e => setPaiementModal(true)}>
                    <i className="fa fa-plus text-primary mr-2" />
                    Ajouter Paiement 
                  </Dropdown.Item>
                  <Dropdown.Item className="dropdown-item" onClick= { e => setClientPresencesModal(true)}>
                    <i className="fa fa-list text-primary mr-2" />
                    {/* <i className="fa fa-clipboard"></i> */}
                     Présences Client
                  </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
        </div>
      </div>
          {/* <div className="row d-flex justify-content-start mb-3 ml-4">
              <div className="btn btn-success ml-4" onClick={e => setPaiementModal(true) }>
                  + Paiement 
              </div>
              <div className="btn btn-danger ml-4" onClick={e => setRenewAbcModal(true)}>
                Renouvelé un abonnement
              </div>
          </div> */}
      <div className="container-fluid" style={{padding: '0px'}}>

      <div className="row d-flex no-gutters ">
      <div className='col-6 col-md-2'>
          <Card >
            <Card.Header style={{padding :'10px 30px'}}>
              <Card.Title>
                <h5>Informations personnelles</h5>
              </Card.Title>
            </Card.Header>
            <Card.Body>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Civilité: <a className="item text-dark"> {client.civility_display}</a> </h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Téléphone:                  <span className="item text-dark"><a href={`tel:${client.phone}`}> {client.phone}</a></span></h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>email:                      <span className="item text-dark"><a href={`mailto:${client.email}`}> {client.email}</a></span></h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Groupe sanguin:&nbsp;&nbsp; <span className="badge badge-danger light">{client.blood}</span> </h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Nationalité:                <span className="item text-dark">{client.nationality}</span> </h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Date de naissance:          <span className="item text-dark">{client.birth_date}</span> </h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Age:                        <span className="item text-dark">{client.age}</span> </h6>
              <h6 className='text-primary' style={{fontSize: '0.9rem'}}>Profession :                <span className="item text-dark">{client.profession}</span> </h6>
              <h5 className='text-primary' style={{fontSize: '0.9rem'}}>Maladies:</h5>
              <ul>
                {client.maladie_name && client.maladie_name.map(maladie =>(
                    <li key={maladie.id} className='ml-2'>{maladie.name}</li>
                  ))}
              </ul>
              <div className="shopping-cart ">
                <h4>Adresse :</h4>
                <p>{client.adress}</p>
              </div>
            </Card.Body>
          </Card>
        </div>
        <div className='col-6 col-md-4'>
          <Card >
            <Card.Header style={{padding :'10px 30px'}}>
              <Card.Title>
                  <div className='ajouter' onClick={e => setClientAbcModal(true)}>Abonnements</div>
           </Card.Title>
               <Card.Title>
                  <div className=' ajouter' onClick= { e => setABCModalCreate(true)}> <i className="fa fa-plus text-primary mr-2" />Ajouter</div>
              </Card.Title>
            </Card.Header>
            <Card.Body>
              <Table responsive striped bordered className="verticle-middle">
                <thead>
                  <tr>
                    <th scope="col">Nom</th>
                    <th scope="col">Séances</th>
                    <th scope="col">Date Début</th>
                    <th scope="col">Date Fin</th>
                    <th scope="col">Prix</th>
                    <th scope="col">Reste</th>
                  </tr>
                </thead>
                <tbody>
                {abonClient.map( abonnement => (
                      <tr className='cursor-abonnement' key={abonnement.id} onClick={e => {
                        setAbonDetailModal(true)
                        setAbonClientID(abonnement.id)
                        setAbonClientType(abonnement.type_abonnement)
                        setAbonClientTypeName(abonnement.type_abonnement_name)
                        setAbonClientEnd(abonnement.end_date)
                        setAbonClientpresences(abonnement.presence_quantity)
                        setAbonnementClientCreneaux(abonnement.creneaux)
                        setAbonClientReste(abonnement.reste)
                      }}>
                      <td className="text-left">{abonnement.type_abonnement_name}</td>
                      <td>{abonnement.is_time_volume ? abonnement.left_minutes : abonnement.is_free_access ? 'Forfait': abonnement.presence_quantity }</td>
                      <td className="text-right">{abonnement.start_date}</td>
                      <td className="text-right">{abonnement.end_date}</td>
                      <td className="text-right">{abonnement.price}</td>
                      <td className="text-left">{abonnement.reste}</td>
                    </tr>
                ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
          </div>
          <div className='col-6 col-md-3'>
          <Card >
            <Card.Header style={{padding :'10px 30px'}}>
              <Card.Title >
                  <div className=' ajouter' onClick={e => setClientPaiementsModal(true)}> Paiements </div>
              </Card.Title>
              <Card.Title>
                  <div className=' ajouter' onClick= { e => setPaiementModal(true)}>   <i className="fa fa-plus text-primary mr-2" />Ajouter</div>
              </Card.Title>
            </Card.Header>
            <Card.Body>
              <Table responsive striped bordered className="verticle-middle">
                <thead>
                  <tr>
                    <th scope="col">Mantant</th>
                    <th scope="col">Date</th>
                    <th scope="col">Abonnement</th>
                    <th scope="col">Reçu</th>
                  </tr>
                </thead>
                <tbody>
                  {transClient.map(trans => (
                    <tr className="ajouter" key={trans.id} onClick={ e => {
                        setPaiementIdInfo(trans.id)
                        setPaiementAmountInfo(trans.amount)
                        setPaiementABCInfo(trans.abc_id)
                        setPaiementABCName(trans.abonnement_name)
                        setPaiementDateInfo(trans.date_creation)
                        setPaiementNotesInfo(trans.notes)
                        }}>
                        <td className="text-left" onClick={e => setPaiementEditModal(true)}>{trans.amount}</td>
                        <td>{trans.date_creation}</td>
                        <td className="text-left">{trans.abonnement_name}</td>
                        <td><ComponentToPrintWrapper item={trans} /></td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
          </div>
          <div className='col-6 col-md-3'>
            <Card >
              <Card.Header style={{padding :'10px 30px'}}>
                <Card.Title >
                  <div className='ajouter' onClick= { e => setClientPresencesModal(true)}> <h4>Seances / Presences</h4> </div>
                </Card.Title>
                <Card.Title>
                    <div className=' ajouter'  onClick= { e => addPresence(true)}> <i className="fa fa-plus text-primary mr-2" />Ajouter</div>
                </Card.Title>
              </Card.Header>
              <Card.Body>
                <Table responsive striped bordered className="verticle-middle">
                  <thead>
                    <tr>
                      <th scope="col">Début</th>
                      <th scope="col">Fin</th>
                      <th scope="col">Jour</th>
                      <th scope="col">Activité</th>
                    </tr>
                  </thead>
                  <tbody>
                  { creneauxClient.map ( creneau => (
                      <tr key={creneau.id}>
                        <td>{creneau.hour_start}</td>
                        <td>{creneau.hour_finish}</td>
                        <td>{creneau.day}</td>
                        <td className="text-left">{creneau.activity_name}</td>
                      </tr>
                      ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
        </div>
        <ABCCreateModal show={aBCmodalCreate} onShowShange={setABCModalCreate} clientData={{clientId: clientId}} />
        <RenewAbonnementModal show={renewAbcModal} onShowShange={setRenewAbcModal} clientData={{clientId: clientId}}/>
        <PaiementsClientModal show={clientPaiementsModal} onShowShange={setClientPaiementsModal} paiementsData={{clientId: clientId}} />
        <PresencesClientModal show={clientPresencesModal} onShowShange={setClientPresencesModal} presencesData={{clientId: clientId}} />
        <AbonnementClientModal show={clientAbcModal} onShowShange={setClientAbcModal} abcData={{clientId: clientId}} />
        <PaiementModal show={paiementModal} onShowShange={setPaiementModal} clientData={{clientId: clientId, abcs :abonClient}} />
        <PaiementEditModal show={paiementEditModal} onShowShange={setPaiementEditModal} paiementData={{clientId: clientId,
          abcs :abonClient,
          paiementIdInfo: paiementIdInfo,
          paiementAmountInfo: paiementAmountInfo,
          paiementABCInfo: paiementABCInfo,
          paiementDateInfo: paiementDateInfo,
          paiementNotesInfo: paiementNotesInfo,
          paiementABCName : paiementABCName,
        }} />
        
        <ABCDetailModal show={abonDetailModal} onShowShange={setAbonDetailModal} abonnementData={{
          clientId: clientId, 
          abonClientID: abonClientID,
          abonClientType : abonClientType,
          abonClientEnd : abonClientEnd,
          abonClientpresences : abonClientpresences,
          abonClientTypeName : abonClientTypeName,
          abonnementClientCreneaux :abonnementClientCreneaux,
          abonClientReste :abonClientReste
          }} />
          <AssuranceCreateModal show={assuranceModal} onShowShange={setAssuranceModal} clientData={{clientId: clientId}}/>
          {/* <AssuranceCreateModal show={assuranceModal} onShowShange={setAssuranceModal} clientData={{clientId: clientId}}/> */}
      </div>
      </div>
    </>
  );
};

export default ProductDetail;
