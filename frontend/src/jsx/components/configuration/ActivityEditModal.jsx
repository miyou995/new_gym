import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";

const ActivityEditModal = ({show, onShowShange, activityData}) => {
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
  const activityEditEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/${activityData['activityId']}/`
  
  const sallesActivite = activityData['salles']
  const selectedSalle  = activityData['salleId']

  const [name, setName] = useState('')
  const [salle, setSalle] = useState('')
  const [allSalles, setAllSalles] = useState('')


const [newSalle, setNewSalle] = useState(selectedSalle)

useEffect(() => {

  if (activityData['activityId']) {
    setName(activityData['activityName'])
    setAllSalles(activityData['salles'])
    setSalle(sallesActivite[activityData['salleId']])
    setNewSalle(sallesActivite[selectedSalle].id)
  }
}, [ activityData['activityId']]);
    const handleSubmit = async e => {
        e.preventDefault();
        const activityFormData = {
            name  : name,
            salle : Number(newSalle),
        }
        await axios.patch(activityEditEND, activityFormData)
        handleShow()
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>modifier l'activité  </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={handleSubmit}>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nom </label>
              <div className="col-sm-9">
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
              </div>
          </div>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Salle </label>
              <div className="col-sm-9">
                  <Autocomplete
                      onChange={((event, value) =>  
                        {
                        setNewSalle(value.id)
                      }
                        )} 
                      // defaultValue={salle}
                      options={allSalles}
                      defaultValue={sallesActivite[selectedSalle]}
                      getOptionSelected={(option) =>  option['id']}
                      id="size-small-standard-multi"
                      getOptionLabel={(option) =>  ( option['name'])}
                      renderInput={(params) =>
                  (<TextField {...params} name="salle" label="salle" variant="outlined" fullWidth />)}
                />
              </div>
          </div>
          <div className="form-group row d-flex justify-content-between">
              <div className="m-3">
                  <button type="submit" className="btn btn-primary">
                      Valider
                  </button>
              </div>
              <div className="m-3">
                  <button type="submit" className="btn btn-danger" onClick={ async () => {
                    await axios.delete(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/delete/${activityData['activityId']}/` )
                    handleShow()}}>
                      Supprimer
                  </button>
              </div>
          </div>
      </form>
     </Modal.Body>
    </Modal>
)}
export default ActivityEditModal;