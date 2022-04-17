import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
 
function refreshPage() {
  window.location.reload(false);
}
const PresenceEditModal = ({show, onShowShange, presenceData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const client  =presenceData['client']
    const clientID  =presenceData['clientId']
    const hourIn  =presenceData['hourIn']
    const hourOut  =presenceData['hourOut']
   //  const creneau  =presenceData['creneau']
    const notes  =presenceData['note']
    const date  =presenceData['date']
    const activity  =presenceData['activity']
    const presenceId = presenceData['presenceId']
    const [hourIn2, setHourIn2] = useState('')
    const [hourOut2,setHourOut2] = useState('')
    const [note,setNote] = useState('')
    const [presenceDate,setPresenceDate] = useState('')


    

    let presenceUpdateEND = `${process.env.REACT_APP_API_URL}/rest-api/presence/${presenceId}/`

    useEffect(() => {
 
      if (show == true) {
         setHourIn2(hourIn)
         setHourOut2(hourOut)
         setNote(notes)
         setPresenceDate(presenceData['date'])
           console.log('THE NEW CLIENT ONEEE ');
      }
        console.log('rani hab naafer creneau DATAAA============>', note,
        hourOut);
    }, [presenceData['presenceId']])


    const handleSubmit = async e => {
      e.preventDefault();
      const newCreneau = {
         hour_entree :hourIn2,
         hour_sortie :hourOut2,
         note :note,
         date :presenceDate,
      }
      // console.log(" =================> new Creneau ", newCreneau);
      await axios.patch(presenceUpdateEND, newCreneau)
    }

return ( 

    <Modal className="fade bd-example-modal-lg" size="lg"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-capitalize text-black'>Presence de <span className='text-danger ml-3 mr-4'> {client}</span> ID: <span className=' ml-1 text-danger'>{clientID}</span></Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span> </Button>
    </Modal.Header>
    <Modal.Body>
      <div>
         <div className="row justify-content-around d-flex m-4">
            <div >
               <h4 className='text-black'>Date : <span className='text-primary'> {date}</span></h4>
               <h4 className='text-black'>Activité : <span className='text-primary'> {activity}</span></h4>
            </div>
            <div>
               <Link className="btn-sm btn-success ml-auto" target='_blank' to={`/client/${clientID}`}>
                  Fiche Client
               </Link>
            </div>
         </div>
         <form onSubmit={handleSubmit}>
            <div className="form-row">
               <div className="form-group col-md-6">
                  <TextField type="time" label="Heure d'entrée" variant="outlined" value={hourIn2} onChange={e=> setHourIn2(e.currentTarget.value)} fullWidth/>
               </div>
               <div className="form-group col-md-6">
                  <TextField type="time" value={hourOut2} variant="outlined" label="Heure de Sortie" fullWidth onChange={e => setHourOut2(e.currentTarget.value)}/>
               </div>
               <div className="form-group col-md-6">
                  <TextField type="text" value={note} label="Note" variant="outlined" onChange={e=> setNote(e.currentTarget.value)} fullWidth/>
               </div>
               <div className="form-group col-md-6">
                  <TextField type="date" value={presenceDate} label="Date" variant="outlined" onChange={e=> setPresenceDate(e.currentTarget.value)} fullWidth/>
               </div>
            </div>
            <div className="row justify-content-md-around">
               <div>
                  <Button onClick={handleShow} variant="danger " > Fermer </Button>
                  <Button variant="primary" type="submit">Sauvgarder</Button>
               </div>
               <div>
                  <Button variant="danger light"  onClick={ async () => {
                    await axios.delete(`${process.env.REACT_APP_API_URL}/rest-api/presence/delete/${presenceId}/`, )
                    handleShow()}}>Supprimé</Button>
               </div>
            </div>
         </form>
      </div>
     </Modal.Body>
   </Modal>
)}
export default PresenceEditModal;