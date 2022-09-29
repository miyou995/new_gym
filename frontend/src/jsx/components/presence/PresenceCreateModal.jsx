import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import { Dropdown, Tab, Navn, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import {notifySuccess, notifyError} from '../Alert'

const PresenceCreateModal = ({show, onShowShange, presenceData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])

    const [samedi, setSamedi] = useState([]);
    const [dimanche, setDimanche] = useState([]);
    const [lundi, setLundi] = useState([]);
    const [mardi, setMardi] = useState([]);
    const [mercredi, setMercredi] = useState([]);
    const [jeudi, setJeudi] = useState([]);
    const [vendredi, setVendredi] = useState([]);
    
    // const presenceId = presenceData['presenceId']
    const [client, setClient] = useState('')
    const [date, setDate] = useState('')
    const [hourIn, setHourIn] = useState('')
    const [hourOut,setHourOut] = useState('')
    const [creneau,setCreneau] = useState('')
    const [note,setNote] = useState('')
    const [showCreneau, setShowCreneau] = useState(false)
    const [selectedAbonnement, setSelectedAbonnement] = useState('')
    
    // const [selectedCreneau, setSelectedCreneau] = useState("")
    // const [creneauActi, setCreneauActi] = useState("")
    // const [creneauCoach, setCreneauCoach] = useState("")
    // const [creneauPlanning, setCreneauPlanning] = useState("")
    // const [creneauDay, setCreneauDay] = useState("")
    // const [startHour, setStartHour] = useState("")
    // const [endHour, setEndHour] = useState("")
    
    
    const formatDate = (date) => {
      return new Date(date).toISOString().slice(0, 10)
   }
    
    
    const [abonnementsClient, setAbonnementsClient] = useState([]);
    // const [selectAbonnement, setSelectAbonnement] = useState("")
    const [selectedCreneau, setSeleCreneau] = useState("")
    
  
  const [clients, setClients] = useState([])
  const [creneaux, setCreneaux] = useState([]);
  const [plannings, setPlannings] = useState([]);
  const [salles, setSalles] = useState([])
  const [salle, setSalle] = useState('')
  const [selectedSalle, setSelectedSalle] = useState(0)
  const [selectedPlanning, setSelectedPlanning] = useState('')
  const [presenceDate, setPresenceDate] = useState(formatDate(new Date()))


  let clientsEND = `${process.env.REACT_APP_API_URL}/rest-api/clients-presence/`
  let presenceCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/presence-create`
  let creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-salle-planning?sa=${selectedSalle}&pl=${selectedPlanning}`
  let sallesEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`
  const creneauClientEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-abc?ab=${selectedAbonnement}`
  let planningsEnd = `${process.env.REACT_APP_API_URL}/rest-api/planning/`

    // let creneauxBySalle = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-salle?salle=${salle}`
    // const abonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    // useEffect(() => {
    //   //  const clientId = props.match.params.id;
    //    const fetchData = async () => {
    //       try {
    //          const res = await api.get(creneauClientEND);
    //          setCreneauxClient(res.data)
   
    //           //console.log('ghirrrr =creneauxClient', creneauxClient);
    //       } catch (error) {
    //          console.log(error, 'erreur presneces');
    //       }
    //    }
    //    fetchData();
    // }, [props.match.params.id] );
    
    useEffect( ()  => {
      if (client !== '') {
         api.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client/?cl=${client}`).then(response => {
          setAbonnementsClient(response.data) ;
          console.log(response.data);
        }).catch(errors => {
           //console.log('erreurs lines 67', errors);
         })
      }
   }, [client]); 
    useEffect( ()  => {
      const fetchData =  () => {
       if (show == true) {
         api.get(planningsEnd).then(responses => {
          setPlannings(responses.data) ;
        }).catch(errors => {
           //console.log('erreurs lines 67', errors);
         })
       }
     }
     fetchData()
   }, [show]); 
   useEffect( ()  => {
    const fetchData = async () => {
     if (show == true) {
      await api.get(clientsEND).then(responses => {
        setClients(responses.data) ;
      }).catch(errors => {
         //console.log('erreurs lines 67', errors);
       })
     }
   }
   fetchData()
 }, [show]); 
  //   useEffect( ()  => {
  //     const fetchData = async () => {

  //      if (show == true) {
  //       await api.get(abonnementEND).then(responses => {
  //         setAbonnements(responses.data) ;
  //       }).catch(errors => {
  //          //console.log('erreurs lines 83', errors);
  //        })
  //      }
  //    }
  //    fetchData()
  //  }, [show]);


    useEffect( ()  => {
      const fetchData =  () => {
       if (show == true) {
         api.get(sallesEnd).then(responses => {
          setSalles(responses.data) ;
        }).catch(errors => {
           //console.log('erreurs lines 98', errors);
         })
       }
     }
     fetchData()
   }, [show]);



   let result1=[]
   let result2=[]
   let result3=[]
   let result4=[]
   let result5=[]
   let result6=[]
   let result7=[]
    useEffect(() => {
      // //console.log('selected salle', typeof selectedSalle );
      if (selectedAbonnement !== '' ) {
        api.get(creneauClientEND).then(res =>{
          //console.log('creneaux end', res.data);
          res.data.forEach((req) => {
          if (req.day == "SA") {
            //console.log('req.day', res.data);
            result1.push(req);
          }else if(req.day== "DI"){
            result2.push(req);
          }else if (req.day== "LU"){
            result3.push(req);
          }else if(req.day== "MA"){
            result4.push(req);
          }else if(req.day== "ME"){
            result5.push(req);
          }else if(req.day== "JE"){
            result6.push(req);
          }else if(req.day== "VE"){
            result7.push(req);
          }
        })
          // setCreneaux([])
          setSamedi(result1)
          setDimanche(result2)
          setLundi(result3)
          setMardi(result4)
          setMercredi(result5)
          setJeudi(result6)
          setVendredi(result7)
        })
      }
    }, [client, selectedAbonnement]);

    // const changingStyle = (id) => {
    //   // const creneau = e.currentTarget.id
    //   // //console.log('the creneay ??? ', creneau);
    //   if (creneaux.indexOf(id) !== -1) {
    //    return true
    //   //  tdClass = 'hett-test'
    //   }
    // }
    
    const changingStyle = (id) => {
      if (creneaux.indexOf(id) !== -1) {
       return true
      }}

    const handleSubmit = async e => {
      e.preventDefault();
      const newCreneau = {
        abc: selectedAbonnement,
        // date : date,:
        hour_entree :  hourIn,
        creneau : creneau,
        note : note,
        // abonnement_client : selectedAbonnement,
        date : formatDate(new Date(presenceDate))
      }
      if (hourOut !== ""){
        newCreneau.hour_sortie = hourOut
      }
      console.log(" =================> new Creneau ", newCreneau);
      await api.post(presenceCreateEND, newCreneau).then( res => {
        notifySuccess('Presence Manuelle enregistré')
        handleShow()
      }).catch( err => {
        console.log('ERRR', err);
        notifyError("erreur de creation de présence, veuillez vérifier les informations manquantes")
      })
    }
    // //console.log('creneaux detail', activities);
return ( 
    <Modal className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-capitalize text-black'>Creation de présence manuellement</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <div>
        <form onSubmit={handleSubmit}>
        <div className="form-row">
        <div className="form-group col- col-md-6">
                <Autocomplete  onChange={(event, value) => {
                        try {
                          setClient(value.id)
                        } catch (error) {
                          setClient('')
                        }}} options={clients} getOptionSelected={(option) =>  option['id']} getOptionLabel={(option) => `${option['id']} -   ${option['first_name']}  ${option['last_name']}  `} renderInput={(params) => 
                  <TextField {...params}  label="Abonné" name="client" variant="outlined" fullWidth />} 
                />
              </div>
              <div className="form-group col- col-md-6">
                <Autocomplete  onChange={(event, value) => {
                        try {
                          setSelectedAbonnement(value.id)
                          setShowCreneau(true)
                        } catch (error) {
                          setSelectedAbonnement('')
                          setShowCreneau(false)
                        }}} options={abonnementsClient} getOptionSelected={(option) =>  option['id']} getOptionLabel={(option) =>  option['type_abonnement_name']} renderInput={(params) => 
                  <TextField {...params}  label="Abonnement" name="abonnement" variant="outlined" fullWidth />} 
                />
              </div>
              {/* <div className="form-group col- col-md-6">
                <Autocomplete  onChange={(event, value) => {
                        try {
                          setSelectedPlanning(value.id)
                        } catch (error) {
                          setSelectedPlanning('')
                          setShowCreneau(false)
                        }}} options={plannings} getOptionSelected={(option) =>  option['id']} getOptionLabel={(option) =>  option['name']} renderInput={(params) => 
                  <TextField {...params}  label="Planning" name="planning" variant="outlined" fullWidth />} 
                />
              </div>
              <div className="form-group col- col-md-6">
                <Autocomplete  onChange={(event, value) => {
                        try {
                          setSelectedSalle(value.id)
                          setShowCreneau(true)
                        } catch (error) {
                          setSelectedSalle(0)
                          setShowCreneau(false)
                        }}} options={salles} getOptionSelected={(option) =>  option['id']} getOptionLabel={(option) =>  option['name']} renderInput={(params) => 
                  <TextField {...params}  label="Salle" name="salle" variant="outlined" fullWidth />} 
                />
              </div> */}

          </div>
          <div className="form-row">
              <div className="form-group col- col-md-6">
                <TextField type="time" label="Heure d'entrée" variant="outlined" value={hourIn} onChange={e=> setHourIn(e.currentTarget.value)}  fullWidth />
              </div>
              <div className="form-group col- col-md-6">
                  <TextField type="time" value={hourOut} variant="outlined" label="Heure de Sortie" fullWidth onChange={e => setHourOut(e.currentTarget.value)} />
              </div>
              <div className="form-group col-6">
                  <TextField type="text" value={note} label="Note" variant="outlined" onChange={e=> setNote(e.currentTarget.value)} fullWidth />
              </div>
              <div className="form-group col-6">
                  {/* <input type="date" className="form-control" value={presenceDate} label="Note" variant="outlined" onChange={e=> setPresenceDate(e.currentTarget.value)} fullWidth /> */}
                  <TextField type="date" className="form-control" value={presenceDate} label="Date" variant="outlined" onChange={e=> setPresenceDate(e.currentTarget.value)} fullWidth />
              </div>
          </div>

          {/* helllloooo */}

    <div className="h-80 mt-3">
         {/* <PageTitle activeMenu="Planning" motherMenu="App" /> */}
         <div>
        { showCreneau &&
        <Col lg={12}>
          <Card>
            
            {/* <Card.Body> */}
            <Table responsive bordered className="verticle-middle">
              <tr>
                <th style={{verticalAlign: "middle", width: "150px", border: ' 1px solid #000000'}}>
                      <h4>Dimanche</h4>
                </th>
                <td>
                  <div>
                { dimanche.map(day=>   ( 
                     <td key={day.id}  style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}   onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setSeleCreneau(day.id)
                      setCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                        <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h6 style={{color: "#ffffff"}}  > {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h6> 
                          <p style={{color: "#ffffff"}}>-{day.coach_name}- {day.activity}</p> 
                        </div>
                      </td> 
                    ))}
                    </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Lundi</h4>
                </th>
                <td style={{ padding: '3px'}}>

                <div>
                { lundi.map(day=>   ( 
                     <td style={{border: "none", width: day.width}} key={day.id}  id={day.id}  onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setSeleCreneau(day.id)  
                      setCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                         <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'}style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Mardi</h4>
                </th>
                <td>
                <div>
                { mardi.map(day=>   ( 
                      
                      <td key={day.id}  style={{border: "none", width: day.width}}  id={day.id}   onClick={e => { if (selectedCreneau === day.id) {
                        setSeleCreneau()
                       }else {
                      setCreneau(day.id)
                      setSeleCreneau(day.id)
                       }
                        // const creneauId = creneaux.indexOf(day.id)
                        // if (creneauId !== -1) {
                        //   const neawCren = creneaux.filter(cren => cren !== day.id)
                        //   setCreneaux(neawCren) 
                        // } else{
                        //   setCreneaux([...creneaux, day.id]) 
                        // }
                      }
                      }
                        >
                          <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                            <h5 style={{color: "#ffffff"}}> {day.hour_start}
                            <span> - </span> 
                            {day.hour_finish}</h5> 
                            <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                          </div>
                        </td> 
                       ))}
                </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Mercredi</h4>
                </th>
                <td>
                <div>
                { mercredi.map(day=>   ( 
                    
                    <td key={day.id}  style={{border: "none", width: day.width}}  id={day.id}  onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setCreneau(day.id)
                      setSeleCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                        <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h5 style={{color: "#ffffff"}}> {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h5> 
                          <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                        </div>
                      </td> 
                     ))}
                </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Jeudi</h4>
                </th>
                <td>
                <div>
                { jeudi.map(day=>   ( 
                     
                     <td  key={day.id}  style={{border: "none", width: day.width}}  id={day.id} onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setCreneau(day.id)
                      setSeleCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                        <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Vendredi</h4>
                </th>
                <td>
                <div>
                { vendredi.map(day=>   ( 
                     <td key={day.id} style={{border: "none", width: day.width}}  id={day.id}  onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setCreneau(day.id)
                      setSeleCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                        <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4>Samedi</h4>
                </th>
                <td>
                <div>
                { samedi.map(day=>   ( 
                    
                    <td key={day.id} style={{border: "none", width: day.width}}  id={day.id}  onClick={e => { if (selectedCreneau === day.id) {
                      setSeleCreneau()
                     }else {
                      setCreneau(day.id)
                      setSeleCreneau(day.id)
                     }
                      // const creneauId = creneaux.indexOf(day.id)
                      // if (creneauId !== -1) {
                      //   const neawCren = creneaux.filter(cren => cren !== day.id)
                      //   setCreneaux(neawCren) 
                      // } else{
                      //   setCreneaux([...creneaux, day.id]) 
                      // }
                    }
                    }
                      >
                        <div className={selectedCreneau===day.id ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h5 style={{color: "#ffffff"}}> {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h5> 
                          <h6 style={{color: "#ffffff"}}>-{day.coach_name}- {day.id}</h6> 
                        </div>
                      </td> 
                     ))}
                </div>
                </td>
              </tr>
              </Table>
              <div>
              
              
              </div>
                
                      
          </Card>
        </Col>
          }
         
         </div>
      </div>
{/* fin table */}
            <Button onClick={handleShow} variant="danger light" className='m-2' > Fermer </Button>
            <Button variant="primary" type="submit">Sauvgarder</Button>
        </form>
      </div>
     </Modal.Body>
    </Modal>
)}
export default PresenceCreateModal;