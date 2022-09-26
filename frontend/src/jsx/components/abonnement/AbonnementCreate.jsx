import React, { useState, useEffect } from "react";
import useAxios from "../useAxios";

import {  useHistory } from "react-router-dom";

 

const AbonnementCreate = (props) => {
  let activityEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`
  
  const api = useAxios();

  
  // let presenceURI = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/${currentPresenceId}/`
  const history = useHistory();
  
  // const [abActivity, setAbActivity] = useState([]);
  const [abName, setAbName] = useState('')
  const [abPrice, setabPrice] = useState('')
  const [abNumDays, setAbNumDays] = useState('')
  const [abSeancesQuantity, setAbSeancesQuantity] = useState('')
  const [selectedActivities, setSelectedActivities] = useState([])
  const [activities, setActivities] = useState([])
  
    //FK 
    useEffect(() => {
      api.get(activityEnd).then((res) => {
        setActivities(res.data)
      })
    }, []);

  //FK 
  // useEffect(() => {
  //   api.get(presenceURI).then((res) => {
    
  //     setAbActivity(res.data.activity)
  //     setAbName(res.data.name)
  //     setabPrice(res.data.price)
  //     setAbNumDays(res.data.length)
  //     setAbSeancesQuantity(res.data.seances_quantity)
  //     setAbActivityName(res.data.activity_name)
  //     setAbNumClients(res.data.clients_number)
  //     console.log('the Presence instance is ======>', res.data);
  // })
  // }, []);


// const setNewAbonnement = () => {
//   if (creneau  === '') {
//     const newClient = {
//       hour_entree:hour_entree,
//       hour_sortie:hour_sortie,
//     }
//     return newClient
//   }else {
//     const newClient = {
//       hour_entree:hour_entree,
//       hour_sortie:hour_sortie,
//       creneau : Number(creneau)

//     }
//     return newClient
//   }
// }
const handleCheckbox = (event) => {
  const activity = event.target.name
    if ( event.target.checked){
      setSelectedActivities(checkedActivities => [...checkedActivities, Number(activity)])
      console.log('maladiieiieiis=======>', selectedActivities);
    }else {
      for ( var i = 0 ; i < selectedActivities.length; i++){
        if (selectedActivities[i] === Number(activity)){
          selectedActivities.splice(i, 1)
        } 
      }
      selectedActivities.splice(Number(activity) , 1)
      console.log('unchecked=======>', selectedActivities);
  }
}


  const HandleSubmit = async e => {
  
    console.log("setSelectedMaladie=======> ", selectedActivities);

  // console.log('les maladiiiies', maladies);
  let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/create`
  e.preventDefault();
  const newAbonnement = {
    activity:selectedActivities,
    name:abName,
    price:abPrice,
    length:abNumDays,
    seances_quantity:abSeancesQuantity,
  }
    api.post(endpoint, newAbonnement).then( () => {
      history.push("/client")
      console.log('THE NEW CLIENT ', newAbonnement);

    })
  }
  return (
        <div className="">
          <div className="card">
            <div className="card-header justify-content-between">
              <h4 className="card-title">Creer un nouvel Abonnement  </h4>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={HandleSubmit}>
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Libellé </label>
                      <input type="text" name="last_name" className="form-control" placeholder="Nom de l'abonnement " onChange={e => setAbName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Prix</label>
                      <input  type="number" name="first_name"  className="form-control"  placeholder="prix "onChange={e => setabPrice(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Nombre de jours</label>
                      <input  type="text" name="first_name"  className="form-control"  placeholder="ex : 30"onChange={e => setAbNumDays(e.target.value)}/>
                    </div>
                  </div>
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Nombre de Séances </label>
                      <input type="number" name="last_name" className="form-control" placeholder="ex: 8" onChange={e => setAbSeancesQuantity(e.target.value)}/>
                    </div>
                  <div className="col-6">
                  <label>
                      Activitées
                    </label>
                    <div className="row">
                          { activities.map(acti =>
                          <div className="col-6">
                                <div className="custom-control custom-checkbox mb-3">
                                  <input type="checkbox" name={acti.id} className="custom-control-input" id={acti.id}  onClick={handleCheckbox}/>
                                  <label className="custom-control-label" htmlFor={acti.id}> {acti.name}</label>
                                </div>
                          </div>
                          )}
                    </div>
                  </div>
                </div>
                  <button type="submit" className="btn btn-primary">
                    Creer
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
  )
}
export default AbonnementCreate;
