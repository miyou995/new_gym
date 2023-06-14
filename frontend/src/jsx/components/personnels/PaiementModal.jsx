import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

const PaiementModal = ({show, onShowChange, coachData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
  const coachId  = coachData['coachId']
     const coachName =  coachData['coachName']
  const paiementCreateEND =`${process.env.REACT_APP_API_URL}/rest-api/transactions/remunerationProf/create` 

  const [amount, setAmount] = useState("")
    const handleSubmit = e => {
      e.preventDefault();
        const paiementDetails = {
          coach  : Number(coachId) ,
          amount : amount
        }
        console.log(" =================> new Creneau ", paiementDetails);
        api.post(paiementCreateEND, paiementDetails).then( res => {
          notifySuccess('Paiement creer avec succés')
                handleShow()
          }).catch(err => {
            notifyError("echec de paiement")
          })
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className="text-black">C
      </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
    <form onSubmit={handleSubmit}>
                  <div className="form-group">
                    <div className="input-group input-group-lg">
                      <div className="input-group-prepend">
                        <span className="input-group-text bg-white border rounded-0">
                          Montant
                        </span>
                      </div>
                      <input
                        type="number"
                        className="form-control rounded-0"
                        placeholder="0000000"
                        onChange={ e => setAmount(e.target.value)}
                      />
                    </div>
                  </div>
                  <Button
                      onClick={handleShow}
                      variant="danger light"
                      className='m-2'
                      >
                      Fermer
                  </Button>
                  <Button variant="primary" type="submit">Valider</Button>
                </form>
     </Modal.Body>
    </Modal>
)

}
export default PaiementModal;