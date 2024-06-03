import React, { useState, useCallback, useEffect } from "react";

import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import useAxios from "../useAxios";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
 

const PaiementsClientModal = ({show, onShowChange, paiementsData}) => {
  const api = useAxios();

    const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
    const [paiements, setPaimeents] = useState([])
    const clientId = paiementsData['clientId']
      const paiementsEnd = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement-by-client/?cl=${clientId}`

    useEffect(() => {
       const fetchData = async () => {
          try {
             const res = await api.get(paiementsEnd);
             setPaimeents(res.data)
          } catch (error) {
             console.log(error);
          }}
       fetchData();
    }, [paiementsData['clientId'], show] );
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" show={show} onHide={handleShow} tabIndex="-1">
    <Modal.Header>
      <Modal.Title className='text-black font-weight-bold'>Paiements du client <span className='test-danger'>{clientId}</span></Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <div className="col-xl-12 col-lg-6">
         <div className="card">
              
            <div className="table-responsive">
               <table className="table">
                  <thead>
                     <tr>
                        <th scope="col"><h5>Mantant</h5></th>
                        <th scope="col"><h5>Abonnement</h5></th>
                        <th scope="col"><h5>Date</h5></th>
                        <th scope="col"><h5>Notes</h5></th>
                     </tr>
                  </thead>
                  <tbody>
                     {paiements.map( paiement => (
                     <tr key={paiement.id}>
                        <td className="font-w600 text-left">{paiement.amount}</td>
                        <td>{paiement.abonnement_name}</td>
                        <td>{paiement.date_creation}</td>
                        <td>{paiement.notes}</td>
                     </tr>
                     ))}
                  </tbody>
               </table>
            </div>
         </div>
      </div>
     </Modal.Body>
    </Modal>
)}
export default PaiementsClientModal;