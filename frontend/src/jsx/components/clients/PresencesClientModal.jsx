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
const PresencesClientModal = ({show, onShowShange, presencesData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const formatDate = (date) => {
      return new Date(date).toISOString().slice(0, 10)
   }
    const [startDate, setStartDate] = useState(formatDate(new Date('2000-01-01')));
   const [endDate, setEndDate] = useState(formatDate(new Date()));
    const [presences, setPresences] = useState([])
    const [presencesCount, setPresencesCount] = useState('')
      const clientId = presencesData['clientId']
      const presencesEnd = `${process.env.REACT_APP_API_URL}/rest-api/presence/client/?cl=${clientId}&start_date=${formatDate(startDate)}&end_date=${formatDate(endDate)}`
   //  useEffect(() => {
   //    // if (paiementsData['clientId']) {
   //       if (show == 'true') {
   //          axios.get(paiementsEnd).then( res => {
   //             setPaimeents(res.data)
   //             console.log('les paiements', paiements, res.data);
   //          })
   //       }
   //    // }
   //  }, [paiementsData['clientId']])
    useEffect(() => {
      //  const clientId = props.match.params.id;
       const fetchData = async () => {
          try {
             const res = await axios.get(presencesEnd);
             setPresences(res.data.results)
             setPresencesCount(res.data.count)
              console.log('ghirrrr =transClient', res.data);
          } catch (error) {
             console.log(error);
          }
       }
       fetchData();
    }, [presencesData['clientId'], endDate] );
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black font-weight-bold'>Presences du client <span className='test-danger'>{clientId}</span> </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
       <div className="row d-flex">
         <div className="form-group col-md-6">
            <label className='text-dark font-weight-bold'>Date de début</label>
            <input type="date" name="start_date" className="form-control" value={startDate}  onChange={e => setStartDate(e.target.value)}/>
         </div>
         <div className="form-group col-md-6">
            <label className='text-dark font-weight-bold'>Date de Fin</label>
            <input type="date" name="end_date" className="form-control" value={endDate}  onChange={e => setEndDate(e.target.value)}/>
         </div>
       </div>
          <th className="text-danger">Total : {presencesCount} </th>
      <div className="col-">
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
                        <th scope="col"><h5>Entrée</h5></th>
                        <th scope="col"><h5>Sortie</h5></th>
                        <th scope="col"><h5>Activité</h5></th>
                        <th scope="col"><h5>Date</h5></th>
                        <th scope="col"><h5>Type</h5></th>

                     </tr>
                  </thead>
                  <tbody>
                     {presences.map( presence => (
                     <tr key={presence.id}>
                        <td className="font-w600 text-left">
                        {presence.hour_entree}
                        </td>
                        <td>
                           {presence.hour_sortie}
                        </td>
                        <td>
                           {presence.client_activity}
                        </td>
                        <td>
                           {presence.date}
                        </td>
                        <td>
                           {presence.abc_name}
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
)

}
export default PresencesClientModal;