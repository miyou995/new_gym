import React, { useState , useEffect, useReducer, useContext} from "react";
import axios from 'axios';
import { Button } from 'react-bootstrap';
import { SalleContext } from './Salle';
import {useGetAPI} from '../useAPI'



const AddSalle = () => {
  const { state, dispatch } = useContext(SalleContext);

  const [salleName, setSalleName] = useState("");
  const [salleAdresse, setSalleAdresse] = useState("");
  const [sallePhone, setSallePhone] = useState("");

  let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/salle-sport/`
  
  const savedSalles = useGetAPI(endpoint)
  
  useEffect(()=>{
    dispatch({type: "get", payload: savedSalles})
  },[savedSalles]) 

  
  const handleSubmit = async e => {
      let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/salle-sport/create`
      e.preventDefault();
      const newSalle = {name:salleName, adresse: salleAdresse, phone: sallePhone}

      await axios.post(endpoint, newSalle)
      dispatch({type:'add', payload:newSalle})
      setSalleName('')
      setSalleAdresse('')
      setSallePhone('')
    }
  return (
    //<div>
      <div>
        {state.salles.map(salle =>  (
       <div >
         <ul key={salle.id}>
           <li>{salle.name}</li>
           <li>{salle.adresse}</li>
           <li>{salle.phone}</li>
         </ul>
         </div>
        ))}
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <form onSubmit={handleSubmit}>
          <input type="text" id="salle_name" name="name" onChange={e => setSalleName(e.target.value)} />
            <label>name</label>
            <br/>
            
            <input type="text" id="salle_adresse" name="adresse" onChange={e => setSalleAdresse(e.target.value)} />
            <label>adresse </label>
            <br/>
          
            <input type="text" name="phone" id="salle_phone" onChange={e => setSallePhone(e.target.value)} />
            <label>phone </label>
            <br/>
            <Button type="submit" >Submit</Button>
        </form>
         


      </div>
  );
}
export default AddSalle ;

