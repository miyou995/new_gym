import React, { Fragment, useState, useEffect , useCallback} from "react";
import { Dropdown, Tab, Nav, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
 
import ShortCuts from "../ShortCuts";

import { ToastContainer } from 'react-toastify'


import useAxios from "../useAxios";
import PerfectScrollbar from "react-perfect-scrollbar";
import {notifySuccess, notifyError} from '../Alert'

import AbonnementCreateModal from './AbonnementCreateModal';
import AbonnementEditModal from './AbonnementEditModal';
import SalleActiviteCreateModal from './SalleActiviteCreateModal'
import PlanningCreateModal from './PlanningCreateModal'
import SalleActiviteEditModal from './SalleActiviteEditModal'
import ActivityCreateModal from './ActivityCreateModal'
import ActivityEditModal from './ActivityEditModal'
import PlanningEditModal from './PlanningEditModal'
import AbonnementListModal from './AbonnementListModal'
import MaladieCreateModal from './MaladieCreateModal'
import MaladieEditModal from './MaladieEditModal'
// import DoorModal from './DoorModal'
const Configuration = (props) => {
  const api = useAxios();
  const abonnementsListEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const maladiesEnd = `${process.env.REACT_APP_API_URL}/rest-api/maladies/`
    const doorsEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/door/`
    const activitiesEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`
    const salleActivitiesEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`
    const planningsEND = `${process.env.REACT_APP_API_URL}/rest-api/planning/`
    const startListenEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/start_listening`
    const stopListenEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/stop_listening`
    
    const [ abonnements , setAbonnements] =useState([])
    const [ maladies , setMaladies] =useState([])
    const [ doors , setDoors] =useState([])
    const [selectedActivities, setSelectedActivities] = useState([])

    const [ abonnementListModal , setAbonnementListModal] =useState(false)
    const [ abonnementCreateModal , setAbonnementCreateModal] =useState(false)
    const [ abonnementEditModal , setAbonnementEditModal] =useState(false)
    const [ salleActiviteCreateModal , setSalleActiviteCreateModal] =useState(false)
    const [ salleActiviteEditModal , setSalleActiviteEditModal] =useState(false)
    const [ planningCreateModal , setPlanningCreateModal] =useState(false)
    const [ planningEditModal , setPlanningEditModal] =useState(false)
    const [ activityCreateModal, setActivityCreateModal] = useState(false)
    const [ activityEditModal, setActivityEditModal] = useState(false)
    const [ maladieCreateModal, setMaladieCreateModal] = useState(false)
    const [ maladieEditModal, setMaladieEditModal] = useState(false)
    // const [ doorModal, setDoorModal] = useState(false)

    const [abonnementId, setAbonnementId] = useState('')
    const [activityId, setActivityId] = useState('')
    const [salleId, setSalleId] = useState('')
    const [maladieId, setMaladieId] = useState('')
    const [maladieName, setMaladieName] = useState('')
    const [planId, setPlanId] = useState('')
    const [planName, setPlanName] = useState('')
    const [isDefaultPlanning, setDefaultPlanning] = useState('')
    const [isDefaultSalle, setDefaultSalle] = useState('')
    const [salleName, setSalleName] = useState('')
    const [doorId, setDoorId] = useState('')
    const [doorIp, setDoorIp] = useState('')
    const [doorUsername, setDoorUsername] = useState('')
    const [doorPassword, setDoorPassword] = useState('')

    const [color, setColor] = useState("")
    const [salle, setSalle] = useState("")
    const [initEffect, setInitEffect] = useState(false)
    const [gymStatus, setGymStatus] = useState(false)
    const [activityName, setActivityName] = useState("")
    const [abDuree, setAbDuree] = useState("")

    const [abIdFromList, setAbIdFromList] = useState("")
    const [salllesActivities, setSalllesActivities] = useState([]);
    const [dureeInd, setDureeInd] = useState("");
    const [typeOf, setTypeOf] = useState("");
    const [activityColor, setActivityColor] = useState("");
    
    
    const [activities, setActivities] = useState([])
    const DureeAb = [
        {mois :'1 Jour', jours : 1},
        {mois :'15 Jour', jours : 15},
        {mois :'45 Jour', jours : 45},
        {mois :'1 mois', jours : 30},
        {mois :'2 mois', jours : 60},
        {mois :'3 mois', jours : 90},
        {mois :'4 mois', jours : 120},
        {mois :'6 mois', jours : 180},
        {mois :'12 mois', jours : 360},
      ]

    useEffect(() => {
        api.get(maladiesEnd).then(res =>{
            setMaladies(res.data)
            console.log('Maladies', res.data);
        })
    }, [maladieCreateModal, maladieEditModal, maladiesEnd]);

    useEffect(() => {
        api.get(activitiesEND).then(res =>{
            setActivities(res.data)
        })
    }, [activitiesEND, activityCreateModal, activityEditModal]);

    useEffect(() => {
        api.get(salleActivitiesEND).then(res =>{
            setSalllesActivities(res.data)
        })
    }, [salleActiviteCreateModal, salleActivitiesEND, salleActiviteEditModal]);

    // useEffect(() => {
    //     api.get(doorsEnd).then(res =>{
    //         setDoors(res.data)
    //     })
    // }, [doorModal]);
    useEffect(() => {
        console.log('dureee de labonnement', DureeAb.findIndex(x => x.jours === Number(abDuree)));
     }, [abDuree, abonnementCreateModal]);

    // const salllesActivities = useGetAPI(salleActivitiesEND)
    const [plannings, setPlannings] = useState([]);
    useEffect(() => {
    api.get(planningsEND).then(res => {
        setPlannings(res.data)
        console.log('plannings', res.data);
    })
    }, [planningEditModal, planningCreateModal, planningsEND]);

    const getAbonnementsActitivties = (actiAbon) => {
        const provActiId = []
        const indexesList = []
        for (let i = 0; i < salllesActivities.length; i++) {
          const element = salllesActivities[i];
          provActiId.push(element.id)
        }
        console.log(provActiId);
        for (let i = 0; i < actiAbon.length; i++) {
          const acti = actiAbon[i];
          const index = provActiId.indexOf(acti) 
          // console.log('indexes', indexes);
          indexesList.push(salllesActivities[index])
        }
        return indexesList    
    }
    const setSelectedSalle = (salles, salleId ) => {
        for (let i = 0; i < salles.length; i++) {
            if (salleId == salles[i].id){
               return i
            }            
        }
    }
    const openTheGym = () => {
        if (gymStatus === false) {
            api.get(startListenEND).then(res => {
                notifySuccess('Toutes les Portes sont activé')
                setGymStatus(true)
              }).catch( err => {
                notifyError("Erreur lors de l'ouverture des portes, veuillez contacter le support'")
              })
        }else{
            notifyError('Toutes les Portes sont déja activé')
        }
    }
    const closeTheGym = () => {
        if (gymStatus === true) {
            api.get(stopListenEND).then(res => {
                notifySuccess('Toutes les Portes sont Désactivé')
                setGymStatus(true)
              }).catch( err => {
                notifyError("Erreur lors de la fermeture des portes, veuillez contacter le support'")
              })
        }else{
            notifyError('Toutes les Portes sont déja Désactivé')
        }
    }

    const getFkIndex = (list,selctedItem) => {
        for (let i = 0; i < list.length; i++) {
          if (selctedItem === list[i].id){
              console.log('the activiti salle ID',i);
             return i
            }            
        }
      }

//  testFunc is the function to send data from child to parent # is triggered from the child
    const TestFunc = useCallback((abId, acti) =>  {
        if (abId !== '') {
            setAbIdFromList(abId)
            setAbonnementId(abId)
            setSelectedActivities(getAbonnementsActitivties(acti))
            setAbonnementEditModal(true)
            }
        }, [abonnementListModal])

    const getDureeIndex = (duree) => {
        const laDuree =DureeAb.findIndex(x => x.jours === duree)
        console.log('selected duree', duree);
        return laDuree
    }
    useEffect(() => {
        //  const clientId = props.match.params.id;
         const fetchData = async () => {
            try {
               const res = await api.get(abonnementsListEND);
               setAbonnements(res.data)
                console.log('ghirrrr =creneauxClient', abonnements);
            } catch (error) {
               console.log(error, 'erreur presneces');
            }
         }
         fetchData();
      }, [props.match.params.id, abonnementEditModal, abonnementCreateModal] );
      console.log('selected activities', selectedActivities);
   return (
      <Fragment>
         <>
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
            <div className="row d-flex justify-content-around m-3">
                <div>
                    <Button className="btn btn-success" onClick={ e => {openTheGym()}}>Ouvrir La salle</Button>
                </div>
                <div>
                    <Button className="btn btn-danger" onClick={ e => {closeTheGym()}}>Fermer La salle</Button>
                {/* <Button onClick={ closeTheGym()}>fermé La salle</Button> */}
                </div>
            </div>
            <div className="row no-gutters">
                <div className="col-lg-2 col-sm-6">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Planning</h4>
                            <Button onClick={e => { setPlanningCreateModal(true)}}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                        <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th>Nom du planning </th>
                    </tr>
                  </thead>
                  <tbody>
                  {plannings.map( plan => (
                    <tr className='cursor-abonnement text-left' key={plan.id} onClick={e => {
                        // setplanActiviteEditModal(true)
                        setPlanId(plan.id)
                        setPlanName(plan.name)
                        setDefaultPlanning(plan.is_default)
                        setPlanningEditModal(true)
                        // setSelectedActivities(getsallesActitivties(salle.activity))
                    }}>
                      <td >{plan.name}</td>
                    </tr>
                  ))}
                  </tbody>
                </table>
                        </div>
                    </div>
                </div>
                <div className="col-lg-2 col-sm-6">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Salle</h4>
                            <Button onClick={e => { 
                                setSalleActiviteCreateModal(true)
                                
                                }}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                        <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th>Nom de la salle </th>
                      <th>Adresse IP</th>
                    </tr>
                  </thead>
                  <tbody>
                  {salllesActivities.map( salle => (
                    <tr className='cursor-abonnement text-left' key={salle.id} onClick={e => {
                        setInitEffect(true)
                        setSalleActiviteEditModal(true)
                        setSalleId(salle.id)
                        setDefaultSalle(salle.is_default)
                        setSalleName(salle.name)
                        setDoorId(getFkIndex(doors, salle.door))
                        setDoorIp(salle.get_adress)
                        console.log(initEffect)
                        // setSelectedActivities(getsallesActitivties(salle.activity))
                    }}>
                      <td >{salle.name}</td>
                      <td >{salle.get_door}</td>
                    </tr>
                  ))}
                    </tbody>
                    </table>
                        </div>
                    </div>
                </div>
                {/* type abonnement va au modal */}
                <div className="col-xl-4 col-lg-4">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Activitées</h4>
                            <Button onClick={e => { setActivityCreateModal(true)}}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                            <PerfectScrollbar   style={{ height: "370px" }}   id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
                                <div className="table-responsive card-table">
                                    <table className="table text-center bg-warning-hover">
                                        <thead>
                                            <tr>
                                                <th className="text-left">Nom</th>
                                                <th >Salle</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        {activities.map( activity => (
                                            <tr className='cursor-abonnement' key={activity.id} onClick={e => {
                                                setActivityEditModal(true)
                                                setActivityId(activity.id)
                                                setActivityName(activity.name)
                                                setColor(activity.color)
                                                setSalleId(getFkIndex(salllesActivities, activity.salle))
                                            }}>
                                                <td className="text-left">{activity.name}</td>
                                                <td >{activity.salle_name}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            </PerfectScrollbar>
                        </div>
                    </div>
                </div>
                {/* DEBUT MALADIES */}
                <div className="col-xl-4 col-lg-4">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Maladies</h4>
                            <Button onClick={e => { setMaladieCreateModal(true)}}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                            <PerfectScrollbar   style={{ height: "370px" }}   id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
                                <div className="table-responsive card-table">
                                    <table className="table text-center bg-warning-hover">
                                        <thead>
                                            <tr>
                                                <th className="text-left">Nom</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        {maladies.map( maladie => (
                                            <tr className='cursor-abonnement' key={maladie.id} onClick={e => {
                                                setMaladieEditModal(true)
                                                setMaladieId(maladie.id)
                                                setMaladieName(maladie.name)
                                            }}>
                                                <td className="text-left">{maladie.name}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            </PerfectScrollbar>
                        </div>
                    </div>
                </div>
                {/* FIN MALADIES */}
                 {/* DEBUT portes */}
                 {/* <div className="col-xl-4 col-lg-4">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Portes</h4>
                            <Button onClick={e => { 
                                setDoorModal(true)
                                setDoorId('')
                                setDoorIp('')
                                setDoorUsername('')
                                setDoorPassword('')
                                }}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                            <PerfectScrollbar   style={{ height: "370px" }}   id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
                                <div className="table-responsive card-table">
                                    <table className="table text-center bg-warning-hover">
                                        <thead>
                                            <tr>
                                                <th className="text-left">Nom</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        {doors.map( door => (
                                            <tr className='cursor-abonnement' key={door.id} onClick={e => {
                                                setDoorModal(true)
                                                setDoorId(door.id)
                                                setDoorIp(door.ip_adress)
                                                setDoorUsername(door.username)
                                                setDoorPassword(door.password)
                                            }}>
                                                <td className="text-left">{door.ip_adress}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            </PerfectScrollbar>
                        </div>
                    </div>
                </div> */}
                {/* FIN portes */}
                <div className=" col-lg-6 config-tableaux">
                    <div className="card">
                        <div className="card-header">
                            <h4  className="card-title ajouter">Type D'abonnement</h4>
                            <Button onClick={e => { setAbonnementCreateModal(true)}}>Ajouter</Button>
                        </div>
                        <div className="card-body">
                            <PerfectScrollbar   style={{ height: "370px" }}   id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
                                <div className="table-responsive card-table">
                                    <table className="table text-center bg-warning-hover config-tableaux">
                                        <thead>
                                            <tr>
                                                <th className="text-left">Abonnement</th>
                                                <th>Durée <br /> <small>(seances/ heures)</small></th>
                                                <th className="text-right">Nombre d'activités'</th>
                                                <th >Inscrits</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        {abonnements.map( abonnement => (
                                            <tr className='cursor-abonnement' key={abonnement.id} onClick={ async e => {
                                                setAbonnementEditModal(true)
                                                setAbonnementId(abonnement.id)
                                                setSelectedActivities(getAbonnementsActitivties(abonnement.salles))
                                                setAbDuree(abonnement.length)
                                                setTypeOf(abonnement.type_of)
                                                setDureeInd(getDureeIndex(abonnement.length))
                                            }}>
                                                <td className="text-left">{abonnement.name}</td>
                                                <td>{abonnement.seances_quantity}</td>
                                                <td className="text-right">{abonnement.salles.length}</td>
                                                <td className="text-right">{abonnement.clients_number}</td>
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            </PerfectScrollbar>
                        </div>
                    </div>
                </div>
            </div>
        <div className="row">
            
        {/* <div className="col-xl-6 col-lg-12">
                    <div className="card">
                        <div className="card-header">
                            <h4 className="card-title">Activités</h4>
                        </div>
                        <div className="card-body">
                            <div className="basic-form">
                                <form onSubmit={(e) => e.preventDefault()}>
                                    <div className="form-group row">
                                        <label className="col-sm-3 col-form-label">Nom de la salle</label>
                                        <div className="col-sm-9">
                                        <input type="text" className="form-control" placeholder="..." />
                                        </div>
                                    </div>
                                    <div className="form-group row">
                                        <div className="col-sm-10">
                                            <button type="submit" className="btn btn-primary">
                                                Valider
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div> */}
                
        </div>
        <AbonnementCreateModal show={abonnementCreateModal} onShowShange={setAbonnementCreateModal} abonnementData={{abonnementId: abonnementId}} />
        <ActivityCreateModal show={activityCreateModal} onShowShange={setActivityCreateModal} activityData={{
            activityId: activityId, 
            salllesActivities : salllesActivities
            }} />
        <ActivityEditModal show={activityEditModal} onShowShange={setActivityEditModal} activityData={{
            activityId: activityId, 
            salllesActivities : salllesActivities, 
            color:color, 
            salle: salle, 
            activityName: activityName, 
            salles: salllesActivities, 
            salleId:salleId}} />
        <SalleActiviteCreateModal  show={salleActiviteCreateModal} onShowShange={setSalleActiviteCreateModal}  salleData={{doors : doors}} />
        <PlanningCreateModal  show={planningCreateModal} onShowShange={setPlanningCreateModal}  />
        <MaladieCreateModal  show={maladieCreateModal} onShowShange={setMaladieCreateModal}  />
        <MaladieEditModal  show={maladieEditModal} onShowShange={setMaladieEditModal} maladieData={{
            maladieId : maladieId,
            maladieName : maladieName
        }} />
        {/* <DoorModal  show={doorModal} onShowShange={setDoorModal} doorData={{
            doorId : doorId,
            doorIp : doorIp,
            doorUsername: doorUsername,
            doorPassword: doorPassword
        }} /> */}
        <PlanningEditModal  show={planningEditModal} onShowShange={setPlanningEditModal} planningData={{
            planId : planId,
            planName :planName,
            isDefaultPlanning: isDefaultPlanning,
        }}  />
        < AbonnementListModal  show={abonnementListModal} onShowShange={setAbonnementListModal} abonnementData={TestFunc} />
        < SalleActiviteEditModal  show={salleActiviteEditModal} onShowShange={setSalleActiviteEditModal}  salleData={{
            salleId : salleId,
            salleName : salleName,
            isDefaultSalle : isDefaultSalle,
            doors : doors,
            doorId : doorId,
            doorIp : doorIp,
            }} />
        <AbonnementEditModal show={abonnementEditModal} onShowShange={setAbonnementEditModal} 
        abonnementData={
            {
            abonnementId: abonnementId,
            selectedActivities: selectedActivities,
            activities : activities,
            salles: salllesActivities, 
            dureeInd: dureeInd,
            // typeOf : typeOf
            }
            } />
         </>
      </Fragment>
   );
};

export default Configuration;
