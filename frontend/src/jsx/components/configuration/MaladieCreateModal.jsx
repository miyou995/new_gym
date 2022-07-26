import React, { useState, useCallback } from "react";
import { Button, Modal } from "react-bootstrap";

import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

const MaladieCreateModal = ({show, onShowShange}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
  const api = useAxios();
  const maladieCreateEnd = `${process.env.REACT_APP_API_URL}/rest-api/maladie/create/`

const [name, setName] = useState('')
    const HandleSubmit = async e => {
        e.preventDefault();
        await api.post(maladieCreateEnd, {name : name}).then( res => {
            notifySuccess('Maladie creer avec succés')
                  handleShow()
            }).catch(err => {
              notifyError("Erreur lors de la creation de la Maladie")
            })
        }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer une nouvelle maladie </Modal.Title>
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
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
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
export default MaladieCreateModal;