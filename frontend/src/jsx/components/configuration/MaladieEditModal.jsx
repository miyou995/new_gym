import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI, usePostAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";

const MaladieEditModal = ({show, onShowShange, maladieData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const maladieUpdateEnd = `${process.env.REACT_APP_API_URL}/rest-api/maladie/${maladieData['maladieId']}`
    const [name, setName] = useState('')
    const [is_default, setDefault] = useState(false)

    useEffect(() => {
      if (show == true) {
          setName(maladieData['maladieName'])
      }
    }, [maladieData['maladieId']]);
    const HandleSubmit = e => {
        e.preventDefault();
        axios.put(maladieUpdateEnd,  {name : name}).then( res => {
            notifySuccess('Maladie modifier avec succés')
                handleShow()
            }).catch(err => {
                notifyError("Erreur lors de la modification de la maladie")
            })
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Modifier la maladie {maladieData['maladieName']}</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={HandleSubmit}>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nom  </label>
              <div className="col-sm-9">
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
              </div>
          </div>

          <div className="form-group row d-flex justify-content-between">
            <div className="m-3">
                <button type="submit" className="btn btn-primary">
                    Valider
                </button>
            </div>
            <div className="m-3">
                <button type="button" className="btn btn-danger" onClick={ async () => {
                await axios.delete(`${process.env.REACT_APP_API_URL}/rest-api/maladie/${maladieData['maladieId']}`)
                notifySuccess(`La salle ${maladieData['maladieName']} a été supprimer avec succés`)
                handleShow()
                }}>Supprimer</button>
            </div>
          </div>
      </form>
     </Modal.Body>
    </Modal>
)}

export default MaladieEditModal;