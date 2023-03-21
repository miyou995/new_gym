import React, { useState, useCallback, useEffect } from "react";

import {  Button, Modal } from "react-bootstrap";
import useAxios from "../useAxios";
 
function refreshPage() {
  window.location.reload(false);
}
const AbonnementClientModal = ({show, onShowChange, abcData}) => {
  const api = useAxios();
  const formatDate = (date) => {
      return new Date(date).toISOString().slice(0, 10)
   }
   const today = new Date()
   var before = today.setDate(today.getDate() - 60);
   var after = today.setDate(today.getDate() + 120);
    const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
    const [startDate, setStartDate] = useState(formatDate(before));
    const [endDate, setEndDate] = useState(formatDate(after));
  
    const [abcs, setAbcs] = useState([])
      const clientId = abcData['clientId']
      const abcEnd = `${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client-all/?cl=${clientId}&start=${startDate}&end=${endDate}`
    useEffect(() => {
       const fetchData = async () => {
          try {
             const res = await api.get(abcEnd);
             setAbcs(res.data)
          } catch (error) {
             console.log(error);
          }
       }
       fetchData();
    }, [abcData['clientId'], startDate, endDate] );  
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Abonnements du client <span className='test-danger'>{clientId}</span> </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <div className="col-xl-12 col-lg-6">
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
                        <td>{abc.is_time_volume ? abc.left_minutes : abc.is_free_access ? 'Forfait': abc.presence_quantity }</td>
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