import React, { useState , useEffect} from "react";
import { Link } from "react-router-dom";
// import productData from "../productData";
import useAxios from "../useAxios";

import { Dropdown, Tab, Nav, Button } from "react-bootstrap";
import PerfectScrollbar from "react-perfect-scrollbar";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
import {notifySuccess, notifyError} from '../Alert'

import product1 from "../../../images/product/1.jpg";
import Search from "../../layouts/Search";
import { createContext } from "react";
import PaiementModal from './PaiementModal'
// import RenewAbonnementModal from './RenewAbonnementModal'
const CoachDetail = (props) => {
  const api = useAxios();
  const [coach, setCoach] = useState({});
  //  const [aBCmodalCreate, setABCModalCreate] = useState(false);
   const [paiementModal, setPaiementModal] = useState(false);
  //  const [abonDetailModal, setAbonDetailModal] = useState(false);
  //  const [abonClient, setAbonClient] = useState([]);
   const [transCoach, setTransCoach] = useState([]);
   const [presencesCoach, setPresnecesCoach] = useState([]);
   const [creneauxCoach, setCreneauxCoach] = useState([]);
  //  const [abonClientID, setAbonClientID] = useState("");
  //  const [abonClientType, setAbonClientType] = useState("");
  //  const [abonClientEnd, setAbonClientEnd] = useState("");
  //  const [abonClientpresences, setAbonClientpresences] = useState("");
  const coachID = props.match.params.id;
  const [lastPresence, setLastPresence] = useState('')
  const presenceCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/coachs/create`
  const presenceUpdateEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/coachs/${lastPresence}/`
  const transactionClientEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/remunerationProf-by-coach/?cl=${coachID}`
  const creneauCoachEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-coach?cl=${coachID}`
const presencesCoachEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/by-coachs/?cl=${coachID}`
const coachDetailEnd = `${process.env.REACT_APP_API_URL}/rest-api/coachs/${coachID}/`
  

  // const [error, setError] = useState(false)
  // const [success, setSuccess] = useState(false)
  
  // const notifySuccess = () => {
  //   toast.success('Entrée Enregistré', {
  //     position: 'top-right',
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //   })
  // }

  // const notifySortie = () => {
  //   toast.success('Sortie Enregistré', {
  //     position: 'top-right',
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //   })
  // }

  // const notifyError = () => {
  //   toast.error('erreur lors Presence Coach', {
  //     position: 'top-right',
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //   })
  // }
  // useEffect(() => {
  //   if (error === true) {
  //     notifyError()
  //   }
  //   setError(false)
  // }, [error]);
  // useEffect(() => {
  //   if (success === true) {
  //     notifySuccess()
  //     setSuccess(false)
  //   }
  // }, [success]);
  useEffect(() => {
    //  const clientId = props.match.params.id;
     const fetchData = async () => {
        try {
           const res = await api.get(creneauCoachEND);
           setCreneauxCoach(res.data)
        } catch (error) {
           console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id] );
  useEffect(() => {
    //  const clientId = props.match.params.id;
     api.get(presencesCoachEND).then( res => {
            setPresnecesCoach(res.data)
           })
  }, [props.match.params.id] );
  useEffect(() => {
    //  const clientId = props.match.params.id;
     const fetchData = async () => {
        try {
           const res = await api.get(transactionClientEND);
           setTransCoach(res.data)
 
            console.log('ghirrrr =creneauxClient', transCoach);
        } catch (error) {
           console.log(error, 'erreur presneces');
        }
     }
     fetchData();
  }, [props.match.params.id, paiementModal] );

  const createPresence = () => {
    const Newcoach = {
      coach: Number(coachID)
    }
    api.post(presenceCreateEND, Newcoach).then(
      notifySuccess('Entrée coach Enregistré')
      ).catch(err => {
      notifySuccess('erreur Enregistrement Presence Coach')
    })
  }
  const updatePresence = async () => {
    const Newcoach = {
      coach: Number(coachID)
    }
    await api.put(presenceUpdateEND, Newcoach).then(
      notifySuccess('Sortie coach Enregistré')
      ).catch(err => {
      notifySuccess('erreur Enregistrement Sortie Coach')
    })
  }
  useEffect(() => {
     const fetchData = async () => {
        try {
           const res = await api.get(coachDetailEnd);
           setCoach(res.data)
          //  console.log(res.data, ' COOOOOOOOOO');
           setLastPresence(res.data.last_presence)
        } catch (error) {
           console.log(error);
        }
     }
     fetchData();
  }, [props.match.params.id, paiementModal] );

const capitalizeFirstLetter = (word) => {
   if (word)
       return word.charAt(0).toUpperCase() + word.slice(1);
   return '';
};
  return (
    <>
<div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
<ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
        <ShortCuts />
      </div>
      {/* <div className="page-titles">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/coach">Coachs</Link>
          </li>
          <li className="breadcrumb-item active">
            <Link to="#">ID: {coach.id} - {coach.last_name}</Link>
          </li>
        </ol>
      </div> */}
      <div className="row">
        
      <div className="col-lg-4  col-sm-6">
         <div className="row">
           <div className="col-6">
           <Button
             className="btn ml-3 btn-success rounded-0 mb-2"
             onClick={e => createPresence()}
           >
             Entré
             <svg
               className="ml-4 scale5"
               width={16}
               height={16}
               viewBox="0 0 29 29"
               fill="none"
               xmlns="http://www.w3.org/2000/svg"
             >
               <path
                 d="M5.35182 13.4965L5.35182 13.4965L5.33512 6.58823C5.33508 6.5844 5.3351 6.58084 5.33514 6.57759M5.35182 13.4965L5.83514 6.58306L5.33514 6.58221C5.33517 6.56908 5.33572 6.55882 5.33597 6.5545L5.33606 6.55298C5.33585 6.55628 5.33533 6.56514 5.33516 6.57648C5.33515 6.57684 5.33514 6.57721 5.33514 6.57759M5.35182 13.4965C5.35375 14.2903 5.99878 14.9324 6.79278 14.9305C7.58669 14.9287 8.22874 14.2836 8.22686 13.4897L8.22686 13.4896L8.21853 10.0609M5.35182 13.4965L8.21853 10.0609M5.33514 6.57759C5.33752 5.789 5.97736 5.14667 6.76872 5.14454C6.77041 5.14452 6.77217 5.14451 6.77397 5.14451L6.77603 5.1445L6.79319 5.14456L13.687 5.16121L13.6858 5.66121L13.687 5.16121C14.4807 5.16314 15.123 5.80809 15.1211 6.6022C15.1192 7.3961 14.4741 8.03814 13.6802 8.03626L13.6802 8.03626L10.2515 8.02798L23.4341 21.2106C23.9955 21.772 23.9955 22.6821 23.4341 23.2435C22.8727 23.8049 21.9625 23.8049 21.4011 23.2435L8.21853 10.0609M5.33514 6.57759C5.33513 6.57959 5.33514 6.58159 5.33514 6.5836L8.21853 10.0609M6.77407 5.14454C6.77472 5.14454 6.77537 5.14454 6.77603 5.14454L6.77407 5.14454Z"
                 fill="white"
                 stroke="white"
               />
             </svg>
           </Button>
           </div>
           <div className="col-6">
           <Button
             onClick={e => updatePresence()}
             className="btn btn-danger rounded-0 mb-2"
           >
             Sortie
             <svg
               className="ml-4 scale3"
               width={16}
               height={16}
               viewBox="0 0 21 21"
               fill="none"
               xmlns="http://www.w3.org/2000/svg"
             >
               <path
                 d="M16.9638 11.5104L16.9721 14.9391L3.78954 1.7565C3.22815 1.19511 2.31799 1.19511 1.75661 1.7565C1.19522 2.31789 1.19522 3.22805 1.75661 3.78943L14.9392 16.972L11.5105 16.9637L11.5105 16.9637C10.7166 16.9619 10.0715 17.6039 10.0696 18.3978C10.0677 19.1919 10.7099 19.8369 11.5036 19.8388L11.5049 19.3388L11.5036 19.8388L18.3976 19.8554L18.4146 19.8555L18.4159 19.8555C18.418 19.8555 18.42 19.8555 18.422 19.8555C19.2131 19.8533 19.8528 19.2114 19.8555 18.4231C19.8556 18.4196 19.8556 18.4158 19.8556 18.4117L19.8389 11.5035L19.8389 11.5035C19.8369 10.7097 19.1919 10.0676 18.3979 10.0695C17.604 10.0713 16.9619 10.7164 16.9638 11.5103L16.9638 11.5104Z"
                 fill="white"
                 stroke="white"
               />
             </svg>
           </Button>
           </div>
           </div>
        </div>
        <div className="col-lg-4  col-sm-6">
            <button type='button' className="btn btn-success" onClick= { e => setPaiementModal(true)}>
              <h2 style={{color:'#ffffff',  marginTop:'5px'}} >Ajouter Virement</h2>
            </button>
        </div>
        <div className="col-lg-4  col-sm-6">
            <button type='button' className="btn btn-danger" >
              <h2 style={{color:'#ffffff',  marginTop:'5px'}} > Reste du salaire : {coach.salaire}</h2>
            </button>
        </div>
      </div>
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <div className="row">
              <div className="card-body bg-white ">
                <div className="media profile-bx">
                      <img src={coach.picture} alt="" />
                      <div className="media-body align-items-center">
                        <h2 className="text-black font-w600">
                          {capitalizeFirstLetter(coach.last_name)} {capitalizeFirstLetter(coach.first_name)}
                        </h2>
                        <h4 className="mb-2 text-black">ID: <span className='text-danger'>{coach.id}</span></h4>
                        <h6 className="text-black">
                            inscrit le : <span className="text-primary">{coach.date_added}</span>
                        </h6>
                        <div className="social-icons">
                            <Link
                              to={`/coach/edit/${coachID}`}
                              className="btn btn-outline-dark"
                            >
                              Modifier Profile
                            </Link>
                        </div>
                      </div>
                      <div className="social-icons m-3">
                        <h6 className='text-primary'>Civilité:                   <a className="item text-dark"> {coach.civility_display}</a> </h6>
                        <h6 className='text-primary'>Téléphone:                  <span className="item text-dark"><a href={`tel:${coach.phone}`}> {coach.phone}</a></span></h6>
                        <h6 className='text-primary'>email:                      <span className="item text-dark"><a href={`mailto:${coach.email}`}> {coach.email}</a></span></h6>
                        <h6 className='text-primary'>Groupe sanguin:&nbsp;&nbsp; <span className="badge badge-danger light">{coach.blood}</span> </h6>
                      </div>
                      <div className="social-icons m-3">
                        <h6 className='text-primary'>Nationalité:                 <span className="item text-dark">{coach.nationality}</span> </h6>
                        <h6 className='text-primary'>Date de naissance:           <span className="item text-dark">{coach.birth_date}</span> </h6>
                        <h6 className='text-primary'>Salaire par heure:           <a className="item text-dark"> {coach.pay_per_hour}</a> </h6>
                      </div>
                  </div>
                </div>
                {/*Tab slider End*/}
                <div className="col-xl-9 col-lg-6  col-md-6 col-xxl-7 col-sm-12">
                  <div className="product-detail-content">
                    {/*Product details*/}
                    <div className="new-arrival-content pr">
                      <ul>
                        {/* 
                          { client.maladie_name.map(maladie =>
                            <div className="custom-control custom-checkbox mb-3">
                              <li className="custom-control-label" key={maladie.id} htmlFor={maladie.id}> {maladie.name}</li>
                            </div>
                          )}
                           */}
                      </ul>
                      <div className='row d-flex'>
                        <div className="shopping-cart mt-3 col- col-md-6">
                          <h4>Note :</h4>
                          <p>{coach.note}</p>
                        </div>
                        <div className="shopping-cart mt-3 col- col-md-6">
                          <h4>Adresse :</h4>
                          <p>{coach.adress}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-lg-4  col-sm-6">
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Creneaux</h4>
              
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
                      <th className="text-left">Début</th>
                      <th>Fin</th>
                      <th>Jour</th>
                      <th>Activité</th>
                      {/* <th className="text-right">Total</th> */}
                    </tr>
                  </thead>
                  <tbody>
                    
                    {creneauxCoach.map(creneau => (
                      <tr key={creneau.id}>
                      <td className="text-left">{creneau.hour_start}</td>
                      {/* <td>0.18</td> */}
                      <td>{creneau.hour_finish}</td>
                      <td>{creneau.day}</td>
                      <td>{creneau.activity_name}</td>
                    </tr>
                    ))
                    }
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>

            </div>

          </div>
        </div>
        <div className="col-xl-3 col-xxl-4 col-lg-6 col-sm-6">
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Virements</h4>
              
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
                      <th className="text-left">Mantant</th>
                      <th>Date</th>
                      {/* <th className="text-right">Total</th> */}
                    </tr>
                  </thead>
                  <tbody>
                    
                    {transCoach.map(trans => (
                      <tr key={trans.id}>
                      <td className="text-left">{trans.amount}</td>
                      {/* <td>0.18</td> */}
                      <td className="text-right">{trans.date_creation}</td>
                    </tr>
                    ))
                    }
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>

            </div>
            <div className="card-footer border-0 pt-0 text-center">
              
            </div>
          </div>
        </div>
        <div className="col-xl-4 col-xxl-4 col-lg-6 col-sm-6">
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Presences</h4>
              
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
                      <th className="text-left">Entrée</th>
                      <th>Sortie</th>
                      {/* <th className="text-right">Activité</th> */}
                      <th className="text-right">Date</th>
                    </tr>
                  { presencesCoach.map ( presence => (
                    <tr key={presence.id}>
                      <td className="text-left">{presence.hour_entree}</td>
                      <td>{presence.hour_sortie}</td>
                      {/* <td>{presence.client_activity}</td> */}
                      <td className="text-right">{presence.date}</td>
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
              
            </div>
          </div>
        </div>
        <PaiementModal show={paiementModal} onShowShange={setPaiementModal} coachData={{coachId: coachID, coachName:coach.first_name}} />

      </div>
    </>
  );
};

export default CoachDetail;
