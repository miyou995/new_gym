import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import jwt_decode from "jwt-decode";

import { Link } from "react-router-dom";
/// Scroll
import PerfectScrollbar from "react-perfect-scrollbar";
import { Dropdown } from "react-bootstrap";
// import { LogoutUser } from "../../utils/auth";
import { set } from "js-cookie";
// import { axiosInstance } from "../../utils/auth";
  import AuthContext from "../../context/AuthContext";
import { useContext } from "react";
import axios from "axios";
// import {notifySuccess, notifyError} from '../Alert'
import {notifySuccess, notifyError} from '../../components/Alert'
import ShortCuts from "../../components/ShortCuts";



const Header = ({ textTab, onNote, toggle, onProfile, onNotification, onClick }) => {

  var path = window.location.pathname.split("/");
  var name = path[path.length - 1].split("-");

  var filterName = name.length >= 3 ? name.filter((n, i) => i > 1) : name;
  var finalName = filterName.includes("app")
    ? filterName.filter((f) => f !== "app")
    : filterName.includes("ui")
    ? filterName.filter((f) => f !== "app")
    : filterName;
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const { user, logoutUser } = useContext(AuthContext);

  const [token, setToken] = useState("");
  const [username, SetUsername] = useState("");
  
  const Logout = async e => {
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/auth/logout/blacklist`
    // const authToken = localStorage.getItem('authTokens')
    const authToken =  JSON.parse(localStorage.getItem("authTokens"))
    //console.log('authToken', jwt_decode(localStorage.getItem("authTokens")));
    // //console.log('refresh 2 ', authToken.refresh);
    //console.log('refresh',  JSON.parse(localStorage.getItem("authTokens")).refresh);
    axios.post(endpoint, {refresh :authToken.refresh}).then( () => {
      console.log(authToken.refresh);
      localStorage.removeItem('authTokens');
      // axiosInstance.defaults.headers['Authorization'] = null;
      window.location = "/login";


    }).catch(err => {
      notifyError(err.error)
      //console.log('err =>', err);
    })
  }

// const response = axiosInstance.post('rest-api/auth/logout/blacklist', {
//   refresh_token: localStorage.getItem('refresh_token'),
// });
  let history = useHistory();

  return (
    <div className="header">
      <div className="header-content">
        <nav className="navbar navbar-expand">
          <div className="collapse navbar-collapse justify-content-between">
            <div className="header-left">
              <div
                className="dashboard_bar"
                style={{ textTransform: "capitalize" }}
              >
               {textTab}
              </div>
            </div>
            
            <ul className="navbar-nav header-right">

            <div className="nav-item dropdown header-profile ml-sm-4 ml-2">
              {
                    user ? ( 

                    <span className="dropdown-item ai-icon"style={{ cursor: 'pointer'}}  onClick={(e) => Logout(e)}>
                   Se Déconnecté </span>
                  ) : (
                    <Link className="dropdown-item ai-icon" to={`/login`} >
                    <svg
                      id="icon-logout"
                      xmlns="http://www.w3.org/2000/svg"
                      className="text-danger"
                      width={18}
                      height={18}
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                      <polyline points="16 17 21 12 16 7" />
                      <line x1={21} y1={12} x2={9} y2={12} />
                    </svg> Se Connecter </Link>
                  )}
            </div>

            </ul>
          </div>
        </nav>
      </div>

    </div>
  );
};

export default Header;
