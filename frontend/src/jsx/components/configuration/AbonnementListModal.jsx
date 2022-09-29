import React, { useState, useCallback, useEffect, memo } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";
function refreshPage() {
  window.location.reload(false);
}
const AbonnementListModal = ({show, onShowShange, abonnementData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const abonnementEditEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`

    const [name, setName] = useState('')
    const [price, setPrice] = useState('')
    const [numberOfDays, setNumberOfDays] = useState('')
    const [seancesQuantity, setSeancesQuantity] = useState('')
    const [activities, setActivities] = useState([])
    const [systemeCochage, setSystemeCochage] = useState(false)
    const [abonnements, setAbonnements] = useState([])
    const [abId, setAbId] = useState('')
    const [acti, setActi] = useState([])


    const [ showModal, setShowModal]  = useState(false)

    const abonnementsEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
// const provArray = []
useEffect(() => {
  if (show == true) {
    api.get(abonnementsEND).then(res => {
      setAbonnements(res.data)
      // setName(res.data.name)
      // setPrice(res.data.price)
      // setNumberOfDays(res.data.length)
      //console.log('fedfef', res.data);
    })
  }
  
}, [show]);

// const openCloseModal = useCallback( (abID) => {} ,[onShowShange])
//  had el useEffect trigli probleme ta3 retard hata ikounou 3andha les valeurs bach t3ayet la fonctions
  useEffect(() => { 
    abonnementData(abId, acti)
    handleShow()
  }, [acti]);
  // return indexesList
    // const getSelectedActivities = () => {
    
    //     console.log(
    //         'les activitesss', activity
    //     );
    //   for (let i = 0; i < activity.length; i++) {
    //       // setRealMaladies([...realMaladies, selectedMaladies[i]['id']])
    //       selectedActivities.push(activity[i]['id'])
    //   }
    //   console.log(
    //     // 'les provArray', provArray
    // );
    // //   setSelectedActivities(provArray)
    // }
// const handleDelete = e => {
//     api.delete(abonnementDeleteEND).then(
//         refreshPage(),
//         handleShow()
//     )
// }
    
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>{name}</Modal.Title>
      <Button
          variant=""
          className="close"
          onClick={handleShow}
          >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
    <table className="table text-center bg-warning-hover config-tableaux">
              <thead>
                  <tr>
                      <th className="text-left">Abonnement</th>
                      <th>Nombre de Séance </th>
                      <th >Nombre jours / semaine</th>
                      <th className="text-right">Nombre d'activités'</th>
                      <th >Inscrits</th>
                  </tr>
              </thead>
              <tbody>
              {abonnements.map( abonnement => (
                  <tr className='cursor-abonnement' key={abonnement.id} onClick={() =>{
                    setAbId(abonnement.id)
                    setActi(abonnement.salles)
                    // abonnementData(abId, acti)
                    // handleShow()
                  }
                  } >
                      <td className="text-left">{abonnement.name}</td>
                      <td>{abonnement.seances_quantity}</td>
                      <td >{abonnement.length}</td>
                      <td className="text-right">{abonnement.salles.length}</td>
                      <td className="text-right">{abonnement.clients_number}</td>
                  </tr>
              ))}
              </tbody>
          </table>
     </Modal.Body>

    </Modal>
)

};
export default AbonnementListModal;