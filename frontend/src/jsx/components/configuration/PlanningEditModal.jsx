import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI, usePostAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import {notifySuccess, notifyError} from '../Alert'
import axios from 'axios';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const PlanningEditModal = ({show, onShowShange, planningData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    
    const [is_default, setDefault] = useState(false)
    const [planId, setPlanId] = useState('')
    const [planName, setPlanName] = useState('')
    const planningEditEnd = `${process.env.REACT_APP_API_URL}/rest-api/planning/${planId}/`
    const HandleSubmit = async e => {
        e.preventDefault();
        const planningForm = {
            name : planName,
            is_default : is_default
        }
        console.log('the form', planningForm);
        await axios.put(planningEditEnd, planningForm).then( res => {
            notifySuccess('Planning modifier avec succés')
                handleShow()
            }).catch(err => {
                notifyError("Erreur lors de la modification du Planning")
            })
      }
      useEffect(() => {
        if (show == true) {
            setPlanId(planningData['planId'])
            setPlanName(planningData['planName'])
            setDefault(planningData['isDefaultPlanning'])
        }
      }, [show]);
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer un nouveau Planning </Modal.Title>
      <Button
          variant=""
          className="close"
          onClick={handleShow}
          >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={HandleSubmit}>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nom </label>
              <div className="col-sm-9">
                  <input type="text" value={planName} className="form-control" placeholder="..." onChange={e => setPlanName(e.target.value)}/>
              </div>
          </div>
          <div className="form-group row">
          <FormControlLabel
                control={
                    <Checkbox 
                        checked={is_default}
                        onChange={e=> {
                        setDefault(!is_default)
                            console.log('target value', e.target.value);
                        }}

                        name="checkedB"
                        color="primary"
                    />
                }
                label="Planning par défaut"
            />
          </div>
          <div className="form-group row d-flex justify-content-between">
              <div className="m-3">
                  <button type="submit" className="btn btn-primary">
                      Valider
                  </button>
              </div>
              <div className="m-3">
                  <button type="button" className="btn btn-danger" onClick={ async () => {
                    await axios.delete(`${process.env.REACT_APP_API_URL}/rest-api/planning/delete/${planId}/` )
                    notifySuccess(`Le planning ${planName} a été supprimer avec succés`)
                    handleShow()}}>Supprimer</button>
              </div>
          </div>
      </form>
     </Modal.Body>
    </Modal>
)}
export default PlanningEditModal;