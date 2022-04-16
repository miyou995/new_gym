import React, { useState } from "react";
import { Link } from "react-router-dom";
import jwt_decode from "jwt-decode";

import { axiosInstance} from "../utils/auth";
import {ToastContainer} from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import {notifyError} from '../components/Alert'

const Login = ({ history }) => {
  // const [email, setEmail] = useState("");
  // const [password, setPassword] = useState("");
  // const [token, setToken] = useState("");

	const initialFormData = Object.freeze({
		email: '',
		password: '',
	});
  const [formData, updateFormData] = useState(initialFormData);
  // const [error , setError] = useState("");
  const { email, password } = formData;

  const handleChange = (e) => {
		updateFormData({
			...formData,
			[e.target.name]: e.target.value.trim(),
		});
	};
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem("authTokens")
      ? jwt_decode(localStorage.getItem("authTokens"))
      : null
  );
  // const config = {
  //   headers: {
  //     Accept: "application/json",
  //     "Content-Type": "application/json",
  //   },
  // };

  // const body = JSON.stringify({ email, password });

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log(formData);

		axiosInstance
			.post(`api/token/`, {
				email: formData.email,
				password: formData.password,
			})
			.then((res) => {
				// localStorage.setItem('authTokens', res.data);
				// // localStorage.setItem('refresh_token', res.data.refresh);
				// axiosInstance.defaults.headers['Authorization'] =
				// 	'JWT ' + localStorage.getItem('access_token');
				// // history.push('/');
        if (res.status === 200) {
          console.log("DATAAAAAAA", res.data);
          setAuthTokens(res.data);
          setUser(jwt_decode(res.data.access));
          localStorage.setItem("authTokens", JSON.stringify(res.data));
          history.push("/");
        } else {
          alert("Something went wrong!");
        }
        window.location = "/";
				console.log(res);
				console.log(res.data);
				console.log("response status =>",res.status);
			}).catch(err => {
        notifyError('Errur, veuiller vérivifer vos identifiant')
				console.log("response status  err=>",err);
      })
	};

  return (
    <div className="authincation h-100 p-meddle">
      <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />

      <div className="container h-100">
        <div className="row justify-content-center h-100 align-items-center">
          <div className="col-md-6">
            <div className="authincation-content">
              <div className="row no-gutters">
                <div className="col-xl-12">
                  <div className="auth-form">
                    <h4 className="text-center mb-4">Connecter vous</h4>
                    <form action="" onSubmit={(e) => handleSubmit(e)}>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Email</strong>
                        </label>
                        <input type="text" className="form-control" value={email} name="email" onChange={(e) => handleChange(e)} />
                      </div>
                      <div className="form-group">
                        <label className="mb-1">
                          <strong>Mot de pass</strong>
                        </label>
                        <input type="password" className="form-control" value={password} name="password" onChange={(e) => handleChange(e)} />
                      </div>
                      <div className="form-row d-flex justify-content-between mt-4 mb-2">
                        <div className="form-group">
                          <div className="custom-control custom-checkbox ml-1">
                            <input type="checkbox" className="custom-control-input" id="basic_checkbox_1" />
                            <label className="custom-control-label" htmlFor="basic_checkbox_1" > Remember my preference </label>
                          </div>
                        </div>
                        <div className="form-group">
                          <Link to="/page-forgot-password">
                            Forgot Password?
                          </Link>
                        </div>
                      </div>
                      <div className="text-center">
                        <input type="submit" value="Sign Me In" className="btn btn-primary btn-block" />
                      </div>
                    </form>
                    <div className="new-account mt-3">
                      <p>
                       Vous n'avez pas de compte ?{" "}
                        <Link className="text-primary" to="/register">
                          Creer un compte
                        </Link>
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
  );
};

export default Login;
