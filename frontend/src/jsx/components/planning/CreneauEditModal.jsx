import React, { useState, useCallback, useEffect } from "react";

import { Row, Card, Col, Button, Modal, Tab, Nav } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import { Link } from "react-router-dom";
import {notifySuccess, notifyError} from '../Alert'
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';


const CreneauCreateModal = ({show, onShowShange, creneauData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])

    let creneauUpdateEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/${creneauData['creneauId']}/`
    const creneauDetailEnd = `${process.env.REACT_APP_API_URL}/rest-api/abc-by-creneau?cr=${creneauData['creneauId']}`
    const activities = creneauData['activities']  
    const coachs =  creneauData['coachs']
    const creneauCoach = creneauData['coach'] 
    const creneauActivite = creneauData['activite'] 
    const plannings = creneauData['plannings']  
    const creneauPlanning = creneauData['planning']
    const days = creneauData['days']
    const day = creneauData['day']
    const clients = creneauData['clients']
    const [abc, setAbc] = useState([])
    const startHour = creneauData['startHour']
    const endHour = creneauData['endHour']
    const coachName = creneauData['coachName']
    const creneauName = creneauData['creneauName']
    const creneauColor = creneauData['creneauColor']
    const activityName = creneauData['activityName']
    const jour = creneauData['jour']
    const creneau = creneauData['creneau']
    // const [newActivity, setNewActivity] = useState(activities[creneauActivite].id)
    // const [newCoach, setNewCoach] = useState(coachs[creneauCoach].id)
    // const [newStartHour, setNewStartHour] = useState(startHour)
    // const [newEndHour, setNewEndHour] = useState(endHour)
    // const [newDay, setNewDay] = useState(days[day].day)
    // const [newPlanning, setNewPlanning] = useState(plannings[creneauPlanning].id)

    const [newActivity, setNewActivity] = useState(creneauActivite)
    const [newCoach, setNewCoach] = useState("")
    const [name,setName] = useState("")
    const [newStartHour, setNewStartHour] = useState("")
    const [newEndHour, setNewEndHour] = useState("")
    const [newDay, setNewDay] = useState("")
    const [newPlanning, setNewPlanning] = useState("")
    const [color, setColor] = useState("")
    
    const [newActivityError, setNewActivityError ] = useState(false)
    const [newCoachError, setNewCoachError ] = useState(false)
    const [newDayError, setNewDayError ] = useState(false)
    const [newPlanningError, setNewPlanningError ] = useState(false)
    const [removeColor, setRemoveColor ] = useState(false)

    
    useEffect(() => {
      // api.get(creneauDetailEND).then((res) => {
      //   setCreneauDetail(res.data)
      //   console.log(res.data);
      if (creneauData['creneauId']) {
        setNewActivity(activities[creneauActivite].id)
        try {
           setNewCoach(coachs[creneauCoach].id)
         } catch (error) {
           setNewCoach(coachs[creneauCoach])
        }
        setNewStartHour(startHour)
        setNewStartHour(startHour)
        setNewEndHour(endHour)
        setNewDay(days[day].day)
        setNewPlanning(plannings[creneauPlanning].id)
        setName(creneauName)
        setColor(creneauColor)
        if (creneauColor) {
           setRemoveColor(removeColor)
        } else {
           setRemoveColor(!removeColor)
        }
        console.log('la couleur du creneau getted creneauName=>',creneauName);
        console.log('la couleur du creneau getted setName=>',name);
      }
    }, [creneauData['creneauId']])








    useEffect(() => {
      api.get(creneauDetailEnd).then(res => {
         setAbc(res.data)
         console.log('les abc dee ce creneau sotn ', res.data);
      })
    }, [creneauData['creneauId']]);

    // }, [creneauData['creneauId']]);

    const handleValidation = () => {
      let formIsValid = true;
      //Name
      if(!newActivity){
          formIsValid = false;
          setNewActivityError(true)
        }

      if(!newDay){
          formIsValid = false;
          setNewDayError(true)
        }
      if(!newPlanning){
          formIsValid = false;
          setNewPlanningError(true)
        }

    //  setErrors({errors: errors});
   //   console.log('IS THE FORM VALID ======?', formIsValid);
     return formIsValid;
 }
    const handleSubmit = e => {
      e.preventDefault();
      if (handleValidation()) {
         const newCreneau = {
            hour_start :newStartHour,
            hour_finish :newEndHour,
            day :newDay,
            coach :newCoach,
            planning :newPlanning,
            name :name,
            activity :newActivity,
         }
         // color :color,
      if( removeColor) {
         newCreneau.color = " "
      }else {
         newCreneau.color = color
      }
       console.log(" =================> new Creneau ", newCreneau);
      api.put(creneauUpdateEND, newCreneau).then( res => {
         
      notifySuccess('Créneau modifier avec succés')
          handleShow()
      }).catch(err => {
          notifyError("Erreur lors de la modification du Créneau")
      })
   }
}
return ( 
    <Modal className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className="text-black">
         <div className="row d-flex justify-content-end">
            <div className='row d-flex col-md-11'>
               <div className='col-3'>
                  <span className="text-primary">Coach: </span> {coachName}  
               </div>
               <div className='col-2'>
                  <span className="text-primary">Jour: </span> {jour} 
               </div>
               <div className='col-2'>
                  <span className="text-primary">HD: </span> {startHour} 
               </div>
               <div className='col-2'>
                  <span className="text-primary">HF: </span> {endHour} 
               </div>
               <div className='col-3'>
               <span className="text-primary">Activité: </span> {activityName} 
               </div>
            </div>
         </div>
      </Modal.Title>
      <Modal.Title>
      <div className='col-1'> 
               <Button variant="" className="close" onClick={handleShow} > <span>&times;</span> </Button>
            </div>
      </Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <div>
      <div className="col-xl-12 col-lg-6">
         <div className="card" style={{backgroundColor: '#ffffff'}}>
            <Tab.Container defaultActiveKey="monthly">
               <div className="card-header border-0 d-xl-flex d-lg-block d-md-flex d-sm-flex d-block">
                  <div className="mr-2">
                     <h4 className="fs-20 text-black">Fiche Créneau</h4>
                  </div>
                  <div className="card-action card-tabs mt-3 mt-sm-0">
                     <Nav className="nav nav-tabs" role="tablist">
                        <Nav.Item>
                           <Nav.Link className="nav-link" data-toggle="tab" eventKey="monthly" role="tab" aria-selected="true" > Detail </Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                           <Nav.Link className="nav-link" data-toggle="tab" eventKey="Weekly" role="tab" aria-selected="false" > Abonnées </Nav.Link>
                        </Nav.Item>
                     </Nav>
                  </div>
               </div>
               <div className="card-body p-0 tab-content card-table">
                  <Tab.Content>
                        {/* CRENEAUX DETAIL TAB */}
                     <Tab.Pane eventKey="monthly">
                        {/* <div className="table-responsive m-2"> */}
                           {/* <table className="table">
                           <tbody> */}
                     <form onSubmit={handleSubmit}>
                        <div className="form-row">
                           <div className="form-group col-md-6">
                              <TextField
                                 type="text"
                                 defaultValue={name}
                                 label="Nom du créneau"
                                 variant="outlined"
                                 onChange={e=> setName(e.currentTarget.value)}
                                 // onChange={(event, value) => setNewStartHour(value)}
                                 fullWidth
                              />
                           </div>
                           <div className="form-group col-md-6">
                              <Autocomplete
                                 // id={(option) =>  option['id']}
                                 
                                 //  {try {
                                    //    setNewActivity(value.id)
                                    //    setNewActivityError(false)
                                    //  } catch (error) {
                                       //    setNewActivity('')
                                       //    setNewActivityError(true)
                                       //  }}
                                       // onChange={handleSubmit}
                                 options={activities}
                                 defaultValue={activities[creneauActivite]}
                                 onChange={(event, value) =>  
                                    {try {
                                    setNewActivity(value.id)
                                    setNewActivityError(false)
                                    } catch (error) {
                                       setNewActivity('')
                                       setNewActivityError(true)
                                       }}
                                    }
                                 getOptionSelected={(option) =>  option['id']}
                                 getOptionLabel={(option) =>  option['name']}
                                 renderInput={(params) => <TextField {...params}  label="Activité" variant="outlined" fullWidth />}
                              />
                                 {newActivityError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir une activité </span> }
                           </div>
                           <div className="form-group col-md-6">
                           <Autocomplete
                              onChange={(event, value) =>{
                              try {
                                 setNewCoach(value.id)
                                 setNewCoachError(false)
                                 } catch (error) {
                                 setNewCoach('')
                                 setNewCoachError(true)
                                 }}
                              }
                              options={coachs}
                              defaultValue={coachs[creneauCoach]}
                              getOptionLabel={(option) =>  option['first_name']}
                              renderInput={(params) => <TextField {...params} label="Coach" variant="outlined" />}
                           />
                              {newCoachError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un coach </span> }
                           </div>
                           <div className="form-group col-md-6">
                              <Autocomplete
                                 onChange={(event, value) =>   {
                                 try {
                                 setNewPlanning(value.id)
                                 setNewPlanningError(false)
                                 } catch (error) {
                                 setNewPlanning('')
                                 setNewPlanningError(true)
                                 }}
                                 }
                                 options={plannings}
                                 defaultValue={plannings[creneauPlanning]}
                                 getOptionLabel={(option) =>  option['name']}
                                 renderInput={(params) => <TextField {...params} label="Planning" variant="outlined" />}
                              />
                              {newPlanningError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un planning</span>}
                           </div>
                           <div className="form-group col-md-6">
                           <Autocomplete
                              onChange={(event, value) => {
                              try {
                                 setNewDay(value.day)
                              setNewDayError(false)
                              } catch (error) {
                              setNewDay('')
                              setNewDayError(true)
                              }}
                           
                              }
                              options={days}
                              defaultValue={days[day]}
                              getOptionLabel={(option) =>  option['label']}
                              renderInput={(params) => <TextField {...params} label="Jour" variant="outlined" />}
                           />
                                       {newDayError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un jour </span> }
                           </div>
                           <div className="form-group col-md-6">
                           <TextField
                              type="time"
                              defaultValue={startHour}
                              label="Heure de Début"
                              variant="outlined"
                              onChange={e=> setNewStartHour(e.currentTarget.value)}
                              // onChange={(event, value) => setNewStartHour(value)}
                              fullWidth
                           />
                           </div>
                           
                           <div className="form-group col-md-6">
                           <TextField
                              type="time"
                              defaultValue={endHour}
                              // value={creneauDetail.hour_finish}
                              // className={classes.textField}
                              variant="outlined"
                              label="Heure de Fin"

                              fullWidth
                              // defaultValue={coachs[coach]}
                              onChange={e => setNewEndHour(e.currentTarget.value)}
                           />
                           </div>
                           <div className="form-group col-md-6">
                              <TextField
                                 type="color"
                                 defaultValue={creneauColor}
                                 padding="none"
                                 label="couleur du créneau"
                                 variant="outlined"
                                 onChange={e=> {
                                    setColor(e.currentTarget.value)
                                 }}
                                 // onChange={(event, value) => setNewStartHour(value)}
                                 fullWidth
                              />
                              <FormControlLabel
                                 control={
                                    <Checkbox
                                       checked={removeColor}
                                       onChange={e=> {
                                          setRemoveColor(!removeColor)
                                          console.log('target value', e.target.value);
                                       }}

                                       name="checkedB"
                                       color="primary"
                                    />
                                 }
                                 label="Désactivé la couleur du créneau"
                              />
                                                   
                           </div>
                        </div>
                           <div className="form-group row d-flex justify-content-between">
                              <div className="m-3">
                                 <Button variant="primary" type="submit">Sauvgarder</Button>
                              </div>
                              <div className="m-3">
                                 <Button variant="primary" type="button" className="btn btn-danger ml-auto" onClick={ async () => {
                                    await api.delete(`${process.env.REACT_APP_API_URL}/rest-api/creneau/delete/${creneauData['creneauId']}/`)
                                    handleShow()
                                 }}>Supprimer</Button>
                              </div>
                           </div>
                     </form>
                           {/* </tbody>

                           </table> */}

                        {/* </div> */}
                     </Tab.Pane>
                              {/* END CRENEAUX DETAIL TAB */}
                              {/* CRENEAUX CLIENTS TAB */}
                     <Tab.Pane eventKey="Weekly">
                        <div className="table-responsive">
                           <table className="table">
                           <thead>
                              <tr>
                                 <th className="customer_shop"> ID </th>
                                 <th>Nom - Prénom </th>
                                 <th> Téléphone </th>
                                 <th> Abonnement </th>
                                 <th> éxpiration </th>
                                 <th> Dettes </th>
                                 <th className='text-right'>FA </th>
                              </tr>
                           </thead>
                           <tbody>
                              {abc.map( ab => (
                              <tr key={ab.id}>
                                 <td>
                                    <div className="media">
                                       <div className="media-body ">
                                          <h5 className="font-w600 text-black">
                                             {ab.client_data.id}
                                          </h5>
                                       </div>
                                    </div>
                                 </td>
                                 <td className="font-w600 ">
                                 <Link className="btn-link text-primary float-left" target="_blank" to={`/client/${ab.client_data.id}`} >
                                    {ab.client_data.last_name} {ab.client_data.first_name} 
                                 </Link>
                                 </td>
                                 <td className="font-w600 text-left">
                                    {ab.client_data.phone ? ab.client_data.phone : '-'}
                                 </td>
                                 <td className="font-w600 text-left">
                                    {ab.abonnement}
                                 </td>
                                 <td className="font-w600 text-left">
                                    {ab.end_date}
                                 </td>
                                 <td className="font-w600 text-danger">
                                    {ab.reste}
                                 </td>
                                 <td className={` ${ab.client_data.fin_assurance ? 'text-right' : 'text-right text-danger'}`}>
                                    {ab.client_data.fin_assurance ? ab.client_data.fin_assurance : 'Non Payés'}
                                 </td>
                              </tr>
                              
                              ))}
                              
                           </tbody>
                           </table>
                        </div>
                     </Tab.Pane>
                              {/* END CRENEAUX CLIENTS TAB */}
                     
                  </Tab.Content>
               </div>
            </Tab.Container>
         </div>
      </div>
   </div>
     </Modal.Body>
    </Modal>
)

}
export default CreneauCreateModal;