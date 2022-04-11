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
const AbonnementClientModal = ({show, onShowShange, abcData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
  
    const [abcs, setAbcs] = useState([])
      const clientId = abcData['clientId']
      const abcEnd = `${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client/?cl=${clientId}`
    useEffect(() => {
       const fetchData = async () => {
          try {
             const res = await axios.get(abcEnd);
             setAbcs(res.data)
          } catch (error) {
             console.log(error);
          }
       }
       fetchData();
    }, [abcData['clientId']] );  
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Abonnements du client <span className='test-danger'>{clientId}</span> </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <div className="col-xl-12 col-lg-6">
         <div className="card">
            {/* <div className="card-header border-0 d-xl-flex d-lg-block d-md-flex d-sm-flex d-block">
                  <h4 className="fs-20 text-black">
                     Fiche Créneau
                  </h4>
            </div> */}
            <div className="table-responsive">
               <table className="table">
                  <thead>
                     <tr>
                        <th scope="col"><h5>Nom</h5></th>
                        <th scope="col"><h5>Type</h5></th>
                        <th scope="col"><h5>Séances</h5></th>
                        <th scope="col"><h5>Date D'éxpiration</h5></th>
                        <th scope="col"><h5>Reste</h5></th>
                     </tr>
                  </thead>
                  <tbody>
                     {abcs.map( abc => (
                     <tr key={abc.id}>
                        <td className="font-w600 text-left">
                        {abc.type_abonnement_name}
                        </td>
                        <td>
                           {abc.cochage ? 'prepayé' : 'Normal'}
                        </td>
                        <td>
                           {abc.presence_quantity}
                        </td>
                        <td>
                           {abc.end_date}
                        </td>
                        <td>
                           {abc.reste}
                        </td>
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
export default AbonnementClientModal;