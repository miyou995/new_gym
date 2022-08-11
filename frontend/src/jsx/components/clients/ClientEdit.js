import React, { useState, useEffect } from "react";
import axios from 'axios';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
// import { useCookies } from 'react-cookie';
import Cookies from 'js-cookie';
import useAxios from "../useAxios";


import {  useHistory } from "react-router-dom";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import {notifySuccess, notifyError} from '../Alert'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export const ClientContext = React.createContext()


function refreshPage() {
  window.location.reload(false);
}


const EditClient = (props) => {
  const api = useAxios();
  let history = useHistory();
  const config = { headers: { 'Content-Type': 'multipart/form-data' } };

  const currentClientId = props.match.params.id;
  let maladiesEnd = `${process.env.REACT_APP_API_URL}/rest-api/maladies/`

  let clientURI = `${process.env.REACT_APP_API_URL}/rest-api/clients/${currentClientId}/`


  // const history = useHistory();
  const [realMaladies, setRealMaladies] = useState([])
  const [maladies, setMaladies] = useState([])
  const [selectedMaladies, setSelectedMaladies] = useState([])
  const [pushedMaladies, setPushedMaladies] = useState([])

  const [civility, setCivility] = useState();
  const [lastName, setLastName] = useState("");
  const [carte, setCarte] = useState("");
  const [firstName, setFirstName] = useState("");
  const [adress, setAdress] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [nationality, setNationality] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [blood, setBlood] = useState("");
  const [note, setNote] = useState("");
  const [etat, setEtat] = useState("");
  const [dette, setDette] = useState("");
  const [gotResult, setGotResult] = useState(false);
const [error, setError] = useState(false)
const [deleted, setDeleted] = useState(false)
const [success, setSuccess] = useState(false)
const [picture, setPicture] = useState(null);


useEffect(() => {
  api.get(maladiesEnd).then((res) => {
    setMaladies(res.data)
  })
}, []);

const getmaladiesNames = (actiAbon) => {
    const provActiId = []
    const indexesList = []
    // const 
    for (let i = 0; i < maladies.length; i++) {
      const element = maladies[i];
      provActiId.push(element.id)
    }
    console.log(provActiId);
    for (let i = 0; i < actiAbon.length; i++) {
      const acti = actiAbon[i];
      const index = provActiId.indexOf(acti) 
      // console.log('indexes', index);
      indexesList.push(maladies[index])

    }
    console.log('indesxxxd', indexesList);
    return indexesList    
}
  useEffect(() => {
  const fetchData =  () => {
     api.get(clientURI).then((res) => {
      setRealMaladies(res.data.maladies)
      setCivility(res.data.civility)
      setLastName(res.data.last_name)
      setFirstName(res.data.first_name)
      setAdress(res.data.adress)
      setPhone(res.data.phone)
      setEmail(res.data.email)
      setNationality(res.data.nationality)
      setBirthDate(res.data.birth_date)
      setBlood(res.data.blood)
      setNote(res.data.note)
      setEtat(res.data.etat)
      setDette(res.data.dette)
      setCarte(res.data.carte)
      // console.log('the real maladies', realMaladies);
      setGotResult(true)
    })
  }
  fetchData()

  }, []);

useEffect(() => {
  if (gotResult == true) {
    setSelectedMaladies(getmaladiesNames(realMaladies))
  }
}, [gotResult]);
useEffect(() => {
  if (success == true) {
    notifySuccess()
  }
}, [success]);

// useEffect(() => {
//   if (deleted == true) {
//     notifyDeleted()
//     setDeleted(false)
//     console.log("this is the deletation ", deleted);
//   }
// }, [deleted]);

// const notifySuccess = () => {
//   toast.success('Profile client modifié Avec Succés', {
//     position: 'top-right',
//     autoClose: 5000,
//     hideProgressBar: false,
//     closeOnClick: true,
//     pauseOnHover: true,
//     draggable: true,
//   })
// }
// const notifyError = () => {
//   toast.error('Echec de la modification', {
//     position: 'top-right',
//     autoClose: 5000,
//     hideProgressBar: false,
//     closeOnClick: true,
//     pauseOnHover: true,
//     draggable: true,
//   })
// }

// const notifyDeleted = () => {
//   toast.success(`le client avec l'id: ${currentClientId} a été supprimer avec succés`, {
//     position: 'top-right',
//     autoClose: 5000,
//     hideProgressBar: false,
//     closeOnClick: true,
//     pauseOnHover: true,
//     draggable: true,
//   })
// }

// useEffect(() => {
//   if (error == true) {
//     notifyError()
//   }
// }, [error]);

const handleImage = (e) => {
  // if (e.target.name === "picture") {
    setPicture({
      image: e.target.files,
      });
    // setPicture(e.target.files[0])
      console.log('e.target.files',e.target.files);
      console.log('e.target.name', e.target.name);
  // }
};
// const deletClient =async () => {
//   const url = `${process.env.REACT_APP_API_URL}/rest-api/clients/delete/${currentClientId}/`
//   await api.delete(url).then(()=>{
//     notifyDeleted()
//       // history.push(`/client/`) 
//     })
// } 



const deletClient =async () => {
  const url = `${process.env.REACT_APP_API_URL}/rest-api/clients/delete/${currentClientId}/`
  await api.delete(url,
   { headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
  }}
    ).then(()=>{
      notifySuccess('Adhérent Supprimé Avec Succée') 
      history.push(`/client/`)
    })
}

const getSelectedMaladies = () => {
  for (let i = 0; i < selectedMaladies.length; i++) {
    // setRealMaladies([...realMaladies, selectedMaladies[i]['id']])
    pushedMaladies.push(Number(selectedMaladies[i]['id']))
  }
}
  const HandleSubmit = async e => {
    getSelectedMaladies()
      e.preventDefault();
      const newMaladies = []
    //   for (let i = 0; i < selectedMaladies.length; i++) {
    //     // setRealMaladies([...realMaladies, selectedMaladies[i]['id']])
    //     console.log('les the sleected madaldie',selectedMaladies);
    //     const maladie = Number(selectedMaladies[i]['id'])
    //     newMaladies.push(maladie) 
    // }
    let formData = new FormData();
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

        // dette :Number(dette),
        pushedMaladies.forEach(item => {
            formData.append('maladies', item);
          })
        if (picture !== null) {
          formData.append('picture', picture.image[0]);
        }
        await api.put(clientURI, formData, config).then(() => {
          setTimeout(()=>{
            notifySuccess('Profile Modifier avec succés')
          }, 100)
          history.push(`/client/${currentClientId}`)
        }).catch((err) => notifyError('Modification profile échoué') )
      }

  return (
  <div className="">
      <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
      <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
          <div className="card">
            <div className="card-header">
              <h4 className="card-title">Profile Abonné</h4>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={HandleSubmit}>
                  <div className="form-row">
                    <div className="form-group  col-md-4 col-xl-3">
                      <label>Carte </label>
                      <input type="text" name="last_name" className="form-control"value={carte}  onChange={e => setCarte(e.target.value)}/>
                    </div>
                    <div className="form-group  col-md-4 col-xl-3">
                      <label>Nom </label>
                      <input type="text" name="last_name" className="form-control"value={lastName}  onChange={e => setLastName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Prénom</label>
                      <input  type="text" name="first_name"  className="form-control" value={firstName} onChange={e => setFirstName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Photo</label>
                      <input type="file" accept="image/*" name="picture"  className="form-control" placeholder="Photo d'identité " onChange={handleImage}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Email </label>
                      <input  type="email" name="email"  className="form-control" value={email === 'null' ? '' : email} placeholder="Email" onChange={e => setEmail(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Adresse</label>
                      <input type="text"name="adress" className="form-control"value={adress} onChange={e => setAdress(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Date de naissance </label>
                      <input type="date" name="birth_date" max="2099-01-01"  className="form-control" value={birthDate}onChange={e => setBirthDate(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Nationalité</label>
                      <input type="text" name="nationality" className="form-control"value={nationality === 'null' ? '' : nationality} onChange={e => setNationality(e.target.value)} />
                    </div>
                    <div className="form-group col-md-4 col-xl-3">
                      <label>Téléphone</label>
                      <input type="text" name="phone" className="form-control" value={phone}onChange={e => setPhone(e.target.value)} />
                    </div>
                    <div className="form-group col-md-2 col-xl-2">
                      <label>Civilité</label>
                      <select defaultValue={"option"} name="civility"  className="form-control" value={civility}onChange={e => setCivility(e.target.value)}>
                      <option value="option" disabled>Cliquez pour choisir</option>
                        <option value="MLL" >Mlle</option>
                        <option value="MME" >Mme</option>
                        <option value="MR" >Mr</option>
                      </select>
                    </div>
                    <div className="form-group col-md-2">
                      <label>Groupe sanguin</label>
                      <select name="blood" className="form-control" value={blood} onChange={e => setBlood(e.target.value)}>
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
                    <div className="form-group col-md-4">
                    <label>Maladies</label>
                    <Autocomplete
                      style={{backgroundColor:'#ffffff'}}
                      multiple
                      onChange={((event, value) =>  
                        {
                          setSelectedMaladies(value)
                        console.log('the valueee', value);
                    }
                        )} 
                      value={selectedMaladies}
                      options={maladies}
                      getOptionLabel={(option) => (option['name'])}
                      renderInput={(params) => (<TextField {...params} name="maladies" variant="outlined" fullWidth />)} />
                    </div>
                  </div>
                  <div className="form-row mb-4">
                      <label>Note</label>
                      <textarea name="note" className="form-control" value={note} onChange={e => setNote(e.target.value)}/>
                  </div>
                  <div className='float-right'>
                  <button type="submit" className="btn btn-primary">
                    Modifier
                  </button>
               </div>
                </form>
                  <button className="btn btn-danger" onClick={deletClient}> Supprimer</button>
              </div>
            </div>
          </div>
        </div>
  )
}
export default EditClient;




