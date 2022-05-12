import React, { Fragment , useState} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
// import DetteCreateModal from './DetteCreateModal';
/// images 
import { Link } from "react-router-dom";
import { useHistory } from 'react-router-dom';
import useAxios from "../useAxios";



const UserCreate = () => {
  const api = useAxios();
  const history = useHistory();
    const initialFormData = Object.freeze({
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      re_password: "",
      });
    const [formData, setFormData] = useState(initialFormData);
  
    const { first_name, last_name, email, password, re_password} = formData;
  
      const handleChange = (e) => {
          setFormData({
              ...formData,
              // Trimming any whitespace
              [e.target.name]: e.target.value.trim(),
          });
      };
      const handleSubmit = (e) => {
          e.preventDefault();
          console.log(formData);
          api.post(`${process.env.REACT_APP_API_URL}/rest-api/auth/register`, {
            email: formData.email,
            first_name:formData.first_name,
            last_name: formData.last_name,
            password: formData.password,
            re_password: formData.re_password,
          })
          .then((res) => {
              window.location = '/login';
              console.log(res);
              console.log(res.data);
          });
      };
   return (
      <Fragment>
         <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />

         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>
         <div className="authincation h-100 p-meddle">
      <div className="container h-100">
        <div className="row justify-content-center h-100 align-items-center">
          <div className="col-md-6">
            <div className="authincation-content">
              <div className="row no-gutters">
                <div className="col-xl-12">
                  <div className="auth-form">
                    <h4 className="text-center mb-4">Creer un nouveau compte</h4>
                    <form onSubmit={(e) => handleSubmit(e)}>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Email</strong>
                        </label>
                        <input type="email" className="form-control" placeholder="hello@example.com" name="email" onChange={(e) => handleChange(e)} value={email} />
                      </div>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Nom</strong>
                        </label>
                        <input type="nom" className="form-control" placeholder="votre nom..." name="first_name" onChange={(e) => handleChange(e)} value={first_name} />
                      </div>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Prénom</strong>
                        </label>
                        <input type="nom" className="form-control" placeholder="votre Prénom..." name="last_name" onChange={(e) => handleChange(e)} value={last_name} />
                      </div>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Password</strong>
                        </label>
                        <input type="password" className="form-control" name="password" onChange={(e) => handleChange(e)} value={password} />
                      </div>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Password</strong>
                        </label>
                        <input type="password" className="form-control" name="re_password" onChange={(e) => handleChange(e)} value={re_password} />
                      </div>
                      <div className="text-center mt-4">
                        <button type="submit" className="btn btn-primary btn-block" > Confirmer </button>
                      </div>
                    </form>
                    <div className="new-account mt-3">
                      <p>
                       Vous avez déja un compte ?{" "}
                        <Link className="text-primary" to="/login">Se connecter</Link>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

        
         
      </Fragment>
   );
};

export default UserCreate;
