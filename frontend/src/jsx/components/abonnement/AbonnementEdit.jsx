import React, { useState, useEffect } from "react";
import useAxios from "../useAxios";

import {  useHistory } from "react-router-dom";

 
function refreshPage() {
  window.location.reload(false);
}
const AbonnementEdit = (props) => {
  let activityEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`
  const api = useAxios();

  const abonnementId = props.match.params.id;
  
  let presenceURI = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/${abonnementId}/`
  let presenceEditURI = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/${abonnementId}/`
  const history = useHistory();
  const [abActivity, setAbActivity] = useState([]);
  const [abName, setAbName] = useState('')
  const [abPrice, setabPrice] = useState('')
  const [abNumDays, setAbNumDays] = useState('')
  const [abSeancesQuantity, setAbSeancesQuantity] = useState('')
  const [abActivityName, setAbActivityName] = useState('')
  const [abNumClients, setAbNumClients] = useState('')
  const [selectedActivities, setSelectedActivities] = useState([])
  const [isSelected, setIsSelected] = useState(true)
  const [activities, setActivities] = useState([])
  
  useEffect(() => {
    api.get(activityEnd).then((res) => {
      setActivities(res.data)
    })
  }, []);

  //FK 
  useEffect(() => {
    api.get(presenceURI).then((res) => {
    
      setAbActivity(res.data.activity)
      setSelectedActivities(res.data.activity)//fzefzefezfezf
      setAbName(res.data.name)
      setabPrice(res.data.price)
      setAbNumDays(res.data.length)
      setAbSeancesQuantity(res.data.seances_quantity)
      setAbActivityName(res.data.activity_name)
      setAbNumClients(res.data.clients_number)
    })
  }, []);
  
  console.log('the Presence instance is ======>',selectedActivities, abActivity);

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
  // const getSelected = (activities, selAct )=> {

  //   for (let i = 0; i < activities.length; i++) {
  //     if ( activities[i] === selAct.id){
  //       console.log('activities[i] === selAct.id', activities[i],selAct.id);
  //       return isSelected ? true : false
  //     }
  //   }
  // }
    // useEffect(() => {

  // }, [selectedActivities]);
  // useEffect(() => {
  //   const initialIsChecked = activities.reduce((selectedActivities,activity) => {
  //     selectedActivities[activity] = false;
  //     return selectedActivities;
  //   }, {})
  //   console.log('the initial state ', initialIsChecked);
  //   setIsSelected(initialIsChecked)
  //   console.log('the initial state ', initialIsChecked);
  // }, [])
  const getSelected = (activity )=> {
    for (let i = 0; i < selectedActivities.length; i++) {
      if ( selectedActivities[i] === activity){
        console.log('activities[i] === selAct.id', selectedActivities[i],selectedActivities, activity);
        return true 
      }
    }
  }

  
const handleCheckbox = (event) => {
  const activity = event.target.name
    if ( event.target.checked){
      setSelectedActivities(checkedActivities => [...checkedActivities, Number(activity)])
      // setAbActivity(checkedActivities => [...checkedActivities, Number(activity)])
      console.log('maladiieiieiis=======>', selectedActivities);
      // setIsSelected(true)
    }else {
      // setIsSelected(false)

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
    console.log('unchecked=======>', selectedActivities);

      e.preventDefault();
      const newAbonnement = {
        name:abName,
        price:abPrice,
        length:abNumDays,
        activity:selectedActivities,
        seances_quantity:abSeancesQuantity,
      }
      api.put(presenceEditURI, newAbonnement).then( () => {
        history.push("/client")
        console.log('THE NEW CLIENT ', newAbonnement);
  
      })
      // history.push("/abonnements")
      // refreshPage()
  }

  return (
        <div className="">
          <div className="card">
            <div className="card-header justify-content-between">
              <div><h4 className="card-title">Abonnement    <span className="text-success">{abName}</span> </h4> </div>
              <div><h4 className="card-title">Nombre d'inscrits    <span className="text-success">{abNumClients}</span> </h4> </div>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={HandleSubmit}>
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Libellé </label>
                      <input type="text" name="last_name" className="form-control"value={abName} placeholder="Nom du client" onChange={e => setAbName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Prix</label>
                      <input  type="text" name="first_name"  className="form-control" value={abPrice} placeholder="Prénom du client"onChange={e => setabPrice(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Nombre de jours</label>
                      <input  type="text" name="first_name"  className="form-control" value={abNumDays} placeholder="Prénom du client"onChange={e => setAbNumDays(e.target.value)}/>
                    </div>
                  </div>
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Nombre de Séances </label>
                      <input type="text" name="last_name" className="form-control"value={abSeancesQuantity} placeholder="Nom du client" onChange={e => setAbSeancesQuantity(e.target.value)}/>
                    </div>
                  
                    <div className="col-6">
                    <label>
                      Activitées
                    </label>
                    <div className="row">
                          { activities.map(acti =>
                          <div key={acti.id} className="col-6">
                                <div className="custom-control custom-checkbox mb-3">
                                  <input checked={getSelected(acti.id)} type="checkbox" name={acti.id} className="custom-control-input" id={acti.id}  onClick={handleCheckbox}/>
                                  <label className="custom-control-label" htmlFor={acti.id}> {acti.name}</label>
                                </div>
                          </div>
                          )}
                    </div>
                  </div>
                  </div>
                  <button type="submit" className="btn btn-primary">
                    Modifier
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      
  )
}
export default AbonnementEdit;



