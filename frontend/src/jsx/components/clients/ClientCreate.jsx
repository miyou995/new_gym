import React, { useState, useEffect } from "react";
import useAxios from "../useAxios";

import {  useHistory } from "react-router-dom";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'

import {notifySuccess, notifyError} from '../Alert'



const CreateClient = () => {
  const api = useAxios();
  const config = { headers: { 'Content-Type': 'multipart/form-data' } };
  let maladiesEnd = `${process.env.REACT_APP_API_URL}/rest-api/maladies/`
  
  const history = useHistory();
  const [selectedMaladies, setSelectedMaladies] = useState([])
  const [civility, setCivility] = useState('MLL');
  const [lastName, setLastName] = useState("");
  const [carte, setCarte] = useState("");
  const [firstName, setFirstName] = useState("");
  const [adress, setAdress] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [nationality, setNationality] = useState("Algérienne");
  const [birthDate, setBirthDate] = useState("");
  const [blood, setBlood] = useState("");
  const [note, setNote] = useState("");
  const [etat, setEtat] = useState("");
  // const [dette, setDette] = useState("");
  
  const [picture, setPicture] = useState(null);
  // const [clientCreated, setClientCreated] = useState(false);
  const [realMaladies, setRealMaladies] = useState([])
  const [maladies, setMaladies] = useState([])
  useEffect(() => {
    api.get(maladiesEnd).then((res) => {
      setMaladies(res.data)
    })
  }, []);
  const handleCheckbox = (event) => {
    const maladie = event.target.name
    if ( event.target.checked){
      setSelectedMaladies(checkedMaladies => [...checkedMaladies, Number(maladie)])
      //console.log('maladiieiieiis=======>', selectedMaladies);
    }else {
      for ( var i = 0 ; i < selectedMaladies.length; i++){
        if (selectedMaladies[i] === Number(maladie)){
          selectedMaladies.splice(i, 1)
        } 
      }
      selectedMaladies.splice(Number(maladie) , 1)
      //console.log('unchecked=======>', selectedMaladies);
  }
}

// useEffect(() => {
//   if (clientCreated == true) {
//     notifyClientCreated()
//     // setClientCreated(false)
//   }
// }, [clientCreated]);


const handleImage = (e) => {
  // if (e.target.name === "picture") {
    setPicture({
      image: e.target.files,
      });
    // setPicture(e.target.files[0])
      //console.log('e.target.files',e.target.files);
      //console.log('e.target.name', e.target.name);
  // }
};
const getSelectedMaladies = ( ) => {
  console.log("REAL MALADIES=======> ", realMaladies);
  console.log("REAL MALADIES=======> ", selectedMaladies);
  for (let i = 0; i < selectedMaladies.length; i++) {
      // setRealMaladies([...realMaladies, selectedMaladies[i]['id']])
    realMaladies.push(selectedMaladies[i]['id'])
  }
}
  const HandleSubmit = async e => {
    getSelectedMaladies()
      // console.log("setSelectedMaladie=======> ", realMaladies);
      console.log("setSelectedMaladie=======> ", realMaladies);
    // //console.log('les maladiiiies', maladies);
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients/create`
    e.preventDefault();
		let formData = new FormData();



    //console.log('the carte', carte);

      formData.append('civility',civility );
      formData.append('carte',carte );
      formData.append('last_name',lastName );
      formData.append('first_name',firstName );
      formData.append('adress',adress );
      formData.append('phone',phone );
      formData.append('email',email );
      formData.append('nationality',nationality );
      formData.append('birth_date',birthDate );
      formData.append('blood',blood );
      formData.append('note',note );
      // formData.append('state',etat );
      // formData.append('dette', Number(dette));

      realMaladies.forEach(item => {
        formData.append('maladies', item);
      })
      if (picture !== null) {
        formData.append('picture', picture.image[0]);
      }else{
        //console.log('il ny a pas de photo', typeof(picture));
      }
      api.post(endpoint, formData, config)
      	.then((res) => {
      		// console.log(res.data);
          history.push("/client")
          notifySuccess('Adhérent Ajouté Avec Succée') 
          //console.log('THE NEW CLIENT ONEEE ', res.data);
      	})
      	.catch((err) => {
          notifyError(`Erreur,  ${err}`)
          //console.log('THE NEW CLIENT ', err.response.data[0])
          //console.log('THE NEW CLIENT ', err.response)
        });
    }

  // let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients/create`

  // const [clientAuth, loading] = useAuth(endpoint, 'POST')

  return (
      <div className="">
         <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
          <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
          <div className="card">
            <div className="card-header">
              <h4 className="card-title">Profile Abonné</h4>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={HandleSubmit}>
                  <div className="form-row">
                    <div className="form-group col-md-6">
                      <label>Carte*</label>
                      <input type="text" name="carte" className="form-control" value={carte} placeholder="Carte de l'adhérent" required onChange={e => setCarte(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Nom*</label>
                      <input type="text" name="last_name" className="form-control" placeholder="Nom de l'adhérent" required onChange={e => setLastName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Photo</label>
                      <input type="file" accept="image/*" name="picture" className="form-control" placeholder="Photo d'identité " onChange={handleImage}/>
                    </div>
                    <div className="form-group col-md-6"> 
                      <label>Prénom</label>
                      <input  type="text" name="first_name"  className="form-control"  placeholder="Prénom de l'adhérent" required onChange={e => setFirstName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Email</label>
                      <input  type="email" name="email"  className="form-control"  placeholder="Email" onChange={e => setEmail(e.target.value)}/>
                    </div>

                    <div className="form-group col-md-6">
                      <label>Adresse</label>
                      <input type="text"name="adress" className="form-control" onChange={e => setAdress(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Date de naissance*</label>
                      <input type="date" name="birth_date" className="form-control" max="2099-01-01" onChange={e => setBirthDate(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Nationalité</label>
                      <input type="text" name="nationality" value={nationality} className="form-control" onChange={e => setNationality(e.target.value)} />
                    </div>
                    <div className="form-group col-md-6">
                      <label>Téléphone*</label>
                      <input type="text" name="phone" className="form-control" onChange={e => setPhone(e.target.value)} />
                    </div>
                  </div>
                
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Civilité*</label>
                      <select  value={civility} name="civility"  className="form-control" onChange={e => setCivility(e.currentTarget.value)}>
                      {/* <option value="option" disabled>Cliquez pour choisir</option> */}
                        <option value="MLL" >Mlle</option>
                        <option value="MME" >Mme</option>
                        <option value="MR" >Mr</option>
                      </select>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Groupe sanguin*</label>
                      <select defaultValue={"option"} name="blood" className="form-control"  onChange={e => setBlood(e.target.value)}>
                      <option value="option" disabled>Cliquez pour choisir</option>
                        <option value='A-' >A-</option>
                        <option value='A+' >A+</option>
                        <option value='B-' >B-</option>
                        <option value='B+' >B+</option>
                        <option value='O-' >O-</option>
                        <option value='O+' >O+</option>
                        <option value='AB-'>AB-</option>
                        <option value='AB+'>AB+</option>
                      </select>
                    </div>
                    {/* <div className="form-group col-md-4">
                      <label>état</label>
                      <select  defaultValue={"option"} name="state" className="form-control" onChange={e => setEtat(e.target.value)}>
                        <option value="option" disabled>Cliquez pour choisir</option>
                        <option value="A" >Active</option>
                        <option value="N" >Non active</option>
                        <option value="S" >Suspendue</option>
                      </select>
                    </div> */}
                     <div className="form-group col-md-4">
                      <label>Maladies</label>
                        <Autocomplete
                            multiple
                            onChange={((event, value) => { 
                                setSelectedMaladies(value) 
                                // console.log(s);
                            //   const maladieId = value.indexOf(value)
                            //   if (maladieId !== -1) {
                            //     const neawCren = value.filter(val => val !== maladieId)
                            //     //console.log('calue de i , id', value.id);
                            //     //console.log('calue de i , vaaal', neawCren);
                            //     //console.log('calue de i , maladieId', maladieId);
                            //     setSelectedMaladies(neawCren) 
                            //   }
                            //   for (let i = 0; i < value.length; i++) {
                               
                            //       setSelectedMaladies([...selectedMaladies, value[i].id])
                            //       //console.log('calue de i , maladieId', maladieId);

                            //       console.log("je suis laaa");
                            // }
                            //console.log('les maladies selectionné', selectedMaladies);
                            })}
                            // onChange={handleSubmit}
                            options={maladies}
                            id="size-small-standard-multi"
                            defaultValue={maladies[9]}
                            //  value={activities[creneauActivite]}
                            // getOptionSelected={(option) =>  option['id']}
                            
                            // getOptionSelected={(option) => //console.log('hello', option.id )}
                            getOptionLabel={(option) =>  (
                                option['name'])}
                            renderInput={(params) =>
                              (<TextField {...params} name="maladies" label="Maladies" variant="outlined" fullWidth />)}
                          />
                      </div>
                  </div>
                    {/* <div className="form-group col-md-4">
                    <label>Dettes</label>
                      <input type="number" name="dette" className="form-control" onChange={e => setDette(e.target.value)}/>
                      <input type="number" name="dette" className="form-control" onChange={e => setDette(e.target.value)}/> 
                    </div> */}
                
                {/* <div className="form-group col-md-4">
                    <label>
                      Maladies
                    </label>
                    <div className="col-4">
                        { maladies.map(maladie =>
                          <div className="custom-control custom-checkbox mb-3">
                            <input type="checkbox" name={maladie.id} className="custom-control-input" id={maladie.id} required onClick={handleCheckbox}/>
                            <label className="custom-control-label" htmlFor={maladie.id}> {maladie.name}</label>
                          </div>
                        )}
                </div> */}
                {/* </div> */}
                 
                  <div className="form-row">
                      <label>Note</label>
                      <textarea name="note" className="form-control" onChange={e => setNote(e.target.value)}/>
                </div>
                  <button type="submit" className="btn btn-primary mt-3">
                    Creer
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
  )
}
export default CreateClient;




