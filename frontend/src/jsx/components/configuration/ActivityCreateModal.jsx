import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import ColorPicker_ from "material-ui-color-picker";
import {notifySuccess, notifyError} from '../Alert'

import createPalette from "@material-ui/core/styles/createPalette";
function refreshPage() {
  window.location.reload(false);
}
const ActivityCreateModal = ({show, onShowChange, activityData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
    // const activitiesEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`
    const activityCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/create`
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`

const [name, setName] = useState('')
const [salle, setSalle] = useState('')
const [color, setColor] = useState("");

    const handleSubmit = e => {
        e.preventDefault();
        const activityFormData = {
            name  : name,
            salle : Number(salle),
            color: color
        }
        api.post(activityCreateEND, activityFormData).then(res => {
          notifySuccess('Activité creer avec succés')
          handleShow()
        }).catch( err => {
          notifyError("Erreur lors de la creation de l'Activité")
        })
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer une nouvelle Activité  </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
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
          
          {/* <div className="form-group row">
              <label className="col-sm-3 col-form-label">Couleur </label>
              <div className="col-sm-9">
              <div className="row">
                <div className="col-xl-4 col-lg-6 mb-3">
                  <div className="example">
                    <input
                      type="color"
                      className="as_colorpicker form-control"
                      value={color}
                      onChange={(e, value) => setColor(e.target.value)}
                    />
                  </div>
                </div>
                
                
              </div>
              </div>
          </div> */}

       
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Salle </label>
              <div className="col-sm-9">
                  <Autocomplete
                      onChange={((event, value) =>  
                        {
                        setSalle(value.id)
                    }
                        )} 
                    //   value={salles}
                      options={activityData['salllesActivities']}
                      getOptionSelected={(option) =>  option['id']}

                      id="size-small-standard-multi"
                      getOptionLabel={(option) =>  ( option['name'])}
                      renderInput={(params) =>
                  (<TextField {...params} name="salle" label="salle" variant="outlined" fullWidth />)}
                />
              </div>
          </div>
          <div className="form-group row">
                <label className="col-sm-3 col-form-label">Couleur</label>
                <div  className="col-sm-9">
                    <input type="color" className="as_colorpicker form-control" value={color} onChange={(e, value) => setColor(e.target.value)} />
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
     </Modal.Body>

    </Modal>
)

}
export default ActivityCreateModal;