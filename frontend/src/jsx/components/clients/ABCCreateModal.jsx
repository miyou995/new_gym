import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
// import api from 'axios';
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

import useAxios from "../useAxios";

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
function refreshPage() {
  window.location.reload(false);
}
const ABCCreateModal = ({show, onShowShange, clientData}) => {
  const api = useAxios();
  const [showCreneau, setShowCreneau] = useState(false)
    const handleShow = useCallback( () => {
      onShowShange(false)
      setShowCreneau(false)
    }, [onShowShange])
    
    
    const clientId = clientData['clientId']
    const today = new Date().toISOString().slice(0, 10)
    const [startDate, setStartDate] = useState(today);
    const [samedi, setSamedi] = useState([]);

    const [dimanche, setDimanche] = useState([]);
    const [lundi, setLundi] = useState([]);
    const [mardi, setMardi] = useState([]);
    const [mercredi, setMercredi] = useState([]);
    const [jeudi, setJeudi] = useState([]);
    const [vendredi, setVendredi] = useState([]);
    
    const [abonnements, setAbonnements] = useState([]);
    
    const [tousLesCreneaux, setTousLesCreneaux] = useState([]);
    
    const [creneaux, setCreneaux] = useState([]);
    const [selectedDays, setSelectedDays] = useState([]);
    // const [day, setDay] = useState([]);
    // const [startDay, setStartDay] = useState(today);
    const [dureeAbonnement, setDureeAbonnement] = useState('');
    const [paiementCochage, setPaiementCochage] = useState(false);
    const [selectAll, setSelectAll] = useState(false);
    
    const [selectAbonnement, setSelectAbonnement] = useState("")
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)
    const [planningId, setPlanningId] = useState("");
    const [plannings, setPlannings] = useState([]);
    
    // let creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-abonnement?ab=${selectAbonnement}`
    let creenauxSallePlanningEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/by-ab-plan?ab=${selectAbonnement}&pl=${planningId}` 
    
    const abonnementClientCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement-client/create`
    const abonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    let planningEND = `${process.env.REACT_APP_API_URL}/rest-api/planning/`

    useEffect(() => {
      api.get(planningEND).then((res) => {
        setPlannings(res.data)
      })
    }, []);
    let result1=[]
    let result2=[]
    let result3=[]
    let result4=[]
    let result5=[]
    let result6=[]
    let result7=[]
    // console.log('the daaaaaays', selectedDays);
    useEffect(() => {
      if (show == true) {
        api.get(abonnementEND).then(res =>{
          setAbonnements(res.data)
        })
      }
    }, [show]);


    useEffect(() => {
      
      if (showCreneau == true) {
        api.get(creenauxSallePlanningEND).then(res =>{
          setTousLesCreneaux(res.data)
          res.data.forEach((req) => {
          if (req.day == "SA") {
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
              setCreneaux([])
              setSamedi(result1)
              setDimanche(result2)
              setLundi(result3)
              setMardi(result4)
              setMercredi(result5)
              setJeudi(result6)
              setVendredi(result7)
            })
      }
    }, [selectAbonnement, planningId]);

    // const notifySuccess = () => {
    //     toast.success('Abonnement Créer Avec Succés', {
    //       position: 'top-right',
    //       autoClose: 5000,
    //       hideProgressBar: false,
    //       closeOnClick: true,
    //       pauseOnHover: true,
    //       draggable: true,
    //     })
    //   }
    // const notifyError = () => {
    //     toast.error('Echec lors de la création', {
    //       position: 'top-right',
    //       autoClose: 5000,
    //       hideProgressBar: false,
    //       closeOnClick: true,
    //       pauseOnHover: true,
    //       draggable: true,
    //     })
    //   }
    //   useEffect(() => {
    //     if (error == true) {
    //       notifyError()
    //     }
    //   }, [error]);
    //   useEffect(() => {
    //     if (success == true) {
    //       notifySuccess()
    //     }
    //   }, [success]);
    const selectAllCreneaux = (creneauxObject) => {
      let creneaux = []
      for (let i = 0; i < creneauxObject.length; i++) {
        const element = creneauxObject[i];
          creneaux.push(element.id)
      }
      return creneaux
    }

    const changingStyle = (id) => {
      if (creneaux.indexOf(id) !== -1) {
       return true
      }}
    function getDayIndex(day){ // this function returns the index of the currente day in the list of days
      switch (day) {
        case 'SA':
            return 6
        case 'DI':
            return 0
        case 'LU':
            return 1
        case 'MA':
            return 2
        case 'ME':
            return 3
        case 'JE':
            return 4
        case 'VE':
            return 5
      }
      }

    const getLastSelectedDay = (selectedStartDate, selectedDays) => {
      let startDate = new Date(selectedStartDate) 
      let theDay = ''
      console.log('dayInd selectedDays ::::', selectedDays);
      for (let i = 0; i < selectedDays.length; i++) {
        // const day = selectedDays[i];
        const dayInd = getDayIndex(selectedDays[i])
        // console.log(' ZERO dayInd', dayInd);
        // console.log('selcted DAYS', selectedDays);
        const dateResult = startDate.setDate((selectedStartDate.getDate()) + (7 + dayInd - selectedStartDate.getDay()) % 7)
        let dateI = new Date(dateResult)
        console.log('  dateRef ===============================>',  dateI);
        if (startDate <=  dateI) {
           theDay = selectedDays[i]
           console.log('resulta intant theDay ', theDay);
      }
          console.log('resulta intant T',  theDay);
      }
      return theDay;
    }
// const getANormalEndDate = (startDate, selectedDays, abonLength ) => {
//     var resultDate = new Date(startDate.getTime());
//     console.log("ONE RESDATE", abonLength);
//     const numDays = Math.floor(abonLength / 7) * 7 - 7
//     console.log("TWO numDays", numDays);
    
//     const AselectedDays = getSelectedDays(creneaux, tousLesCreneaux)
//     console.log("THREE AselectedDays", AselectedDays);
    
//     const returnedDay = getLastSelectedDay(new Date(startDate), AselectedDays)
//     console.log("FOUR returnedDay", returnedDay);
//     const daysNumber = (numDays + getDayIndex(returnedDay)) - (startDate.getDay() % numDays)
//     console.log('daysNumber', daysNumber);
//     const finalDate = resultDate.setDate(resultDate.getDate() + daysNumber);
//     console.log("FIVEEEE returnedDay", new Date(finalDate));
//     return finalDate;
// }
const getCochageEndDate = (startDate, abonLength) => {
  // const someDate = new Date();
  const endDate =  startDate.setDate(startDate.getDate() + abonLength); 
  return endDate
}
const getSelectedDays = (creneauxIds, tousLesCreneaux) => {
  let days = []
  for (let i = 0; i < creneauxIds.length; i++) {
    const item = creneauxIds[i];
    for (let j = 0; j < tousLesCreneaux.length; j++) {
      const element = tousLesCreneaux[j];
      if (item == element.id ) {
        days.push(element.day)
      }
    }
  }
  days = [...new Set(days)]
  return days
}
    const handleSubmit = async e => {
      e.preventDefault();
      const newABC = {
        client :clientId,
        type_abonnement :Number(selectAbonnement),
        start_date: startDate,
        creneaux :creneaux,
      }
      const axWait = await api.post(abonnementClientCreateEND, newABC).then( e => {
        notifySuccess("Abonnement creer avec succés")
        handleShow()
      }).catch(err => {
        notifyError("Erreur lors de la creation de l'abonnement'")
        console.log('the axwait', err);
      })
      return axWait
    }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer un nouvel abonnement pour : {clientId}</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span></Button>
    </Modal.Header>
    <Modal.Body>
        <form onSubmit={handleSubmit}>
        <div className="row">
        <div className="form-group col-md-4">
              <label className='text-dark font-weight-bold'>PLannings</label>
              <select   name="activities" defaultValue={'option'} className="form-control" onChange={e => setPlanningId(e.target.value)  }>
                <option name='option'>Selectionner un planning</option>
                {plannings.map( salle => (
                  <option key={salle.id} value={salle.id} name={salle.name}>{salle.name}</option>
                ))}
              </select>
             </div>
              <div className="form-group col-md-4">
              <label className='text-dark font-weight-bold'>Abonnement Type</label>
                <Autocomplete
                      onChange={(event, value) => 
                        {try {
                          setSelectAbonnement(value.id)
                          setDureeAbonnement(value.length)
                          setPaiementCochage(value.systeme_cochage)
                          setShowCreneau(true)
                        } catch (error) {
                          setSelectAbonnement('')
                          setDureeAbonnement('')
                          setShowCreneau(false)
                        }}
                        }
                      // onChange={handleSubmit}
                      options={abonnements}
                      getOptionSelected={(option) =>  option['id']}
                      getOptionLabel={(option) =>  option['name']}
                      renderInput={(params) => <TextField {...params}  label="..." name="activity" variant="outlined" fullWidth />}
                    />
              </div>
              <div className="form-group col-md-4">
                <label className='text-dark font-weight-bold'>Date de début</label>
                <input type="date" name="start_date"  value={startDate} className="form-control" onChange={e => setStartDate(e.target.value)}/>
              </div>
      </div>
      <div className="row">
          <labelc className='text-dark font-weight-bold' >Selectionner tout</labelc>
          <input className="h-80 ml-3" value={selectAll} type="checkbox" onClick={e => {
            if (selectAll) {
              setSelectAll(false)
              setCreneaux([])
            }else{
              setSelectAll(true)
              setCreneaux(selectAllCreneaux(tousLesCreneaux))
            }
            }}/>
      </div>
    <div className="h-80 mt-3">
         {/* <PageTitle activeMenu="Planning" motherMenu="App" /> */}
         <div>
        { showCreneau &&
        <Col lg={12}>
          <Card style={{backgroundColor: '#ffffff'}}>
            {/* <Card.Body> */}
            <Table responsive bordered className="verticle-middle">
              <tbody>
              { dimanche.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle", width: "150px", border: ' 1px solid #000000'}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Dimanche</h4>
                </th>
                <td>
                  <div>
                { dimanche.map(day=>   ( 
                     <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                      const creneauId = creneaux.indexOf(day.id)
                      if (creneauId !== -1) {
                        const neawCren = creneaux.filter(cren => cren !== day.id)
                        setCreneaux(neawCren) 
                      } else{
                        setCreneaux([...creneaux, day.id]) 
                      }
                      }}>
                        <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h6 style={{color: "#ffffff"}}  > {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h6> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p  className='mb-0'style={{color: "#ffffff"}}>{day.activity_name}</p> 
                        </div>
                      </td> 
                    ))}
                    </div>
                </td>
              </tr>
}
{ lundi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2  text-dark font-weight-bold'>Lundi</h4>
                </th>
                <td style={{ padding: '3px'}}>
                <div>
                { lundi.map(day=>   ( 
                     <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                      const creneauId = creneaux.indexOf(day.id)
                      const creneauDay = selectedDays.indexOf(day.day)
                      if (creneauId !== -1) {
                        const neawCren = creneaux.filter(cren => cren !== day.id)
                        setCreneaux(neawCren) 
                      } else{
                        setCreneaux([...creneaux, day.id]) 
                      }
                      if (creneauDay !== -1) {
                        const neawdays = selectedDays.filter(cren => cren !== day.day)
                        setSelectedDays(neawdays) 
                      } else{
                        setSelectedDays([...selectedDays, day.day]) 
                      }
                      }}>
                         <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'}style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
}
{ mardi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Mardi</h4>
                </th>
                <td>
                <div>
                { mardi.map(day=>   ( 
                      <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                        const creneauId = creneaux.indexOf(day.id)
                        const creneauDay = selectedDays.indexOf(day.day)
                        if (creneauId !== -1) {
                          const neawCren = creneaux.filter(cren => cren !== day.id)
                          setCreneaux(neawCren) 
                        } else{
                          setCreneaux([...creneaux, day.id]) 
                        }
                        if (creneauDay !== -1) {
                          const neawdays = selectedDays.filter(cren => cren !== day.day)
                          setSelectedDays(neawdays) 
                        } else{
                          setSelectedDays([...selectedDays, day.day]) 
                        }
                        }}>
                          <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                            <h5 style={{color: "#ffffff"}}> {day.hour_start}
                            <span> - </span> 
                            {day.hour_finish}</h5> 
                            <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                            <p className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 

                          </div>
                        </td> 
                       ))}
                </div>
                </td>
              </tr>
}
{ mercredi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Mercredi</h4>
                </th>
                <td>
                <div>
                { mercredi.map(day=>   ( 
                   <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                    const creneauId = creneaux.indexOf(day.id)
                    const creneauDay = selectedDays.indexOf(day.day)
                    if (creneauId !== -1) {
                      const neawCren = creneaux.filter(cren => cren !== day.id)
                      setCreneaux(neawCren) 
                    } else{
                      setCreneaux([...creneaux, day.id]) 
                    }
                    if (creneauDay !== -1) {
                      const neawdays = selectedDays.filter(cren => cren !== day.day)
                      setSelectedDays(neawdays) 
                    } else{
                      setSelectedDays([...selectedDays, day.day]) 
                    }

                    }}>
                        <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h5 style={{color: "#ffffff"}}> {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h5> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 
                           
                        </div>
                      </td> 
                     ))}
                </div>
                </td>
              </tr>
}
{ jeudi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Jeudi</h4>
                </th>
                <td>
                <div>
                { jeudi.map(day=>   ( 
                     <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                      const creneauId = creneaux.indexOf(day.id)
                      const creneauDay = selectedDays.indexOf(day.day)
                      if (creneauId !== -1) {
                        const neawCren = creneaux.filter(cren => cren !== day.id)
                        setCreneaux(neawCren) 
                      } else{
                        setCreneaux([...creneaux, day.id]) 
                      }
                      if (creneauDay !== -1) {
                        const neawdays = selectedDays.filter(cren => cren !== day.day)
                        setSelectedDays(neawdays) 
                      } else{
                        setSelectedDays([...selectedDays, day.day]) 
                      }

                      }}>
                         <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <p className='mb-0'  style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p  className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
}
{ vendredi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Vendredi</h4>
                </th>
                <td>
                <div>
                { vendredi.map(day=>   ( 
                    <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                      const creneauId = creneaux.indexOf(day.id)
                      const creneauDay = selectedDays.indexOf(day.day)
                      if (creneauId !== -1) {
                        const neawCren = creneaux.filter(cren => cren !== day.id)
                        setCreneaux(neawCren) 
                      } else{
                        setCreneaux([...creneaux, day.id]) 
                      }
                      if (creneauDay !== -1) {
                        const neawdays = selectedDays.filter(cren => cren !== day.day)
                        setSelectedDays(neawdays) 
                      } else{
                        setSelectedDays([...selectedDays, day.day]) 
                      }

                      }}>
                         <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                           <h5 style={{color: "#ffffff"}}> {day.hour_start}
                           <span> - </span> 
                           {day.hour_finish}</h5> 
                           <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 
                         </div>
                       </td> 
                      ))}
                </div>
                </td>
              </tr>
}
{ samedi.length > 0 &&
              <tr>
                <th style={{verticalAlign: "middle"}}>
                      <h4 className='pl-2 text-dark font-weight-bold'>Samedi</h4>
                </th>
                <td>
                <div>
                { samedi.map(day=>   ( 
                    <td style={{border: "none", width: day.width, maxWidth: '300px', padding : '6px'}}  key={day.id}  onClick={e => { 
                      const creneauId = creneaux.indexOf(day.id)
                      const creneauDay = selectedDays.indexOf(day.day)
                      if (creneauId !== -1) {
                        const neawCren = creneaux.filter(cren => cren !== day.id)
                        setCreneaux(neawCren) 
                      } else{
                        setCreneaux([...creneaux, day.id]) 
                      }
                      if (creneauDay !== -1) {
                        const neawdays = selectedDays.filter(cren => cren !== day.day)
                        setSelectedDays(neawdays) 
                      } else{
                        setSelectedDays([...selectedDays, day.day]) 
                      }

                      }}>
                        <div className={changingStyle(day.id) ? 'selected-creneau fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded': 'fc-event-calendar mt-0 ml-0 mb-2 btn btn-block rounded'} style={{backgroundColor: day.creneau_color}}>
                          <h5 style={{color: "#ffffff"}}> {day.hour_start}
                          <span> - </span> 
                          {day.hour_finish}</h5> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.coach_name}</p> 
                          <p className='mb-0' style={{color: "#ffffff"}}>{day.activity_name}</p> 
                        </div>
                      </td> 
                     ))}
                </div>
                </td>
              </tr>
}
              </tbody>

              </Table>
              <div>
              </div>
          </Card>
        </Col>
          }
         </div>
      </div>
      <Button onClick={handleShow} variant="danger light" className='m-2' > Fermer </Button>
        <Button variant="primary" type="submit">Valider</Button>
      </form>
     </Modal.Body>
    </Modal>
)

}
export default ABCCreateModal;