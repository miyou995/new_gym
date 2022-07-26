import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import {notifySuccess, notifyError} from '../Alert'
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
const PaiementCreateModal = ({show, onShowShange, creneauData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const creneauCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/creneau/create/`

    const [newActivity, setNewActivity] = useState("")
    const [newCoach, setNewCoach] = useState("")
    const [newStartHour, setNewStartHour] = useState("")
    const [newEndHour, setNewEndHour] = useState("")
    const [newDay, setNewDay] = useState("")
    const [newPlanning, setNewPlanning] = useState("")

    const [newActivityError, setNewActivityError ] = useState(false)
    // const [newCoachError, setNewCoachError ] = useState(false)
    const [newDayError, setNewDayError ] = useState(false)
    const [newPlanningError, setNewPlanningError ] = useState(false)
    const [removeColor, setRemoveColor ] = useState(true)
    const [color, setColor] = useState("")
    const [name,setName] = useState("")


    const days = creneauData['days']
    const activities = creneauData['activities']  
    const coachs =  creneauData['coachs']

    const plannings = creneauData['plannings']  

    const handleValidation = () => {
      let errors = {};
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
     console.log('IS THE FORM VALID ======?', formIsValid);
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
      activity :newActivity,
    }
    if(removeColor) {
      newCreneau.color = " "
    }else {
        newCreneau.color = color
    }
    console.log(" =================> new Creneau ", newCreneau);
    api.post(creneauCreateEND, newCreneau).then( res => {
      notifySuccess('Créneau creer avec succés')
          handleShow()
      }).catch(err => {
          notifyError("Erreur lors de la création du créneau")
      })
  }}
    
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className="text-black">Créneau</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span> </Button>
    </Modal.Header>
    <Modal.Body>
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
              onChange={(event, value) => 
                {try {
                  setNewActivity(value.id)
                  setNewActivityError(false)
                } catch (error) {
                  setNewActivity('')
                  setNewActivityError(true)
                }}
               
                }
              // onChange={handleSubmit}
              options={activities}
              getOptionSelected={(option) =>  option['id']}
              getOptionLabel={(option) =>  option['name']}
              renderInput={(params) => <TextField {...params}  label="Activité" name="activity" variant="outlined" fullWidth />}
            />
           {newActivityError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir une activité </span> }
          </div>
          <div className="form-group col-md-6">
          <Autocomplete
            onChange={(event, value) =>
              {
                try {
                setNewCoach(value.id)
                // setNewCoachError(false)
              } catch (error) {
                setNewCoach('')
                // setNewCoachError(true)
              }}
              }
            options={coachs}
            getOptionLabel={(option) =>  option['last_name']}
            renderInput={(params) => <TextField {...params} label="Coach" variant="outlined" />}
            />
            {/* {newCoachError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un coach </span> } */}
          </div>
          <div className="form-group col-md-6">
            <Autocomplete
              onChange={(event, value) => 
                {
                  try {
                    setNewPlanning(value.id)
                    setNewPlanningError(false)
                } catch (error) {
                    setNewPlanning('')
                    setNewPlanningError(true)
                }}
              }
              options={plannings}
              getOptionLabel={(option) =>  option['name']}
              renderInput={(params) => <TextField {...params} label="Planning" variant="outlined" />}
              />
              {newPlanningError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un planning</span> }
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
            getOptionLabel={(option) =>  option['label']}
            renderInput={(params) => <TextField {...params} label="Jour" variant="outlined" />}
            />
            {newDayError &&  <span  style={{color:'#EF5350', fontSize : '14px'}}> Veuillez choisir un jour </span> }
          </div>
          <div className="form-group col-md-6">
          <TextField
            type="time"
            required
          //   defaultValue={startHour}
            label="Heure de Début"
            variant="outlined"
            onChange={e=> 
              {
                try {
                setNewStartHour(e.currentTarget.value)
              } catch (error) {
                setNewStartHour('')
              }}
             
              }
            // onChange={(event, value) => setNewStartHour(value)}
            fullWidth
            />
          </div>
          <div className="form-group col-md-6">
          <TextField
            type="time"
          //   defaultValue={endHour}
            // value={creneauDetail.hour_finish}
            // className={classes.textField}
            variant="outlined"
            label="Heure de Fin"
              required
            fullWidth
            // defaultValue={coachs[coach]}
            onChange={e => 
              {
                try {
                setNewEndHour(e.currentTarget.value)
              } catch (error) {
                setNewEndHour('')
              }}
              }
          />
          </div>
          <div className="form-group col-md-6">
                              <TextField
                                 type="color"
                                //  defaultValue={creneauColor}
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
        <Button onClick={handleShow}variant="danger light"className='m-2'>
            Fermer
        </Button>
        <Button variant="primary" type="submit">Sauvgarder</Button>
        </form>
     </Modal.Body>
    </Modal>
)

}
export default PaiementCreateModal;