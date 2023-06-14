import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useHistory } from "react-router-dom";
import {notifyError} from '../components/Alert'

const AuthContext = createContext();

export default AuthContext;


export const AuthProvider = ({ children }) => {
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
  const [loading, setLoading] = useState(true);
  //console.log('user=> ', user);
  const history = useHistory();
//   console.log("test get user ", localStorage.getItem("access_token"))

  const getTokenEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/login/`
  const registerEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/register/`



  const loginUser = async (email, password) => {
    const response = await fetch(getTokenEnd, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email,
        password
      })
    });
    const data = await response.json();

    if (response.status === 200) {
      setAuthTokens(data);
      setUser(jwt_decode(data.access));
      localStorage.setItem("authTokens", JSON.stringify(data));
      window.location ="/";
    } else {
      // console.log(response);
      notifyError('Veuillez vérifier vos informations de connection')
      // alert("Ohhh went wrong!");
    }
  };
  
  const registerUser = async (email, password, password2) => {
    const response = await fetch(registerEnd, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email,
        password,
        password2
      })
    });
    if (response.status === 201) {
      window.location ="/login";
    } else {
      notifyError('Veuillez vérifier vos informations de connection')
      // alert("Something went wrong!");
    }
  };
  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    window.location ="/login";
  };

  const contextData = {
    user:user,
    authTokens:authTokens,
    setAuthTokens:setAuthTokens,
    setUser:setUser,
    loginUser:loginUser,
    logoutUser:logoutUser,
    registerUser:registerUser,
  };
// //console.log('USERRRR', user);
useEffect(() => {
  if (authTokens) {
    setUser(jwt_decode(authTokens.access));
  }
  setLoading(false);
}, [authTokens, loading]);

return (
  <AuthContext.Provider value={contextData}>
    {loading ? null : children}
  </AuthContext.Provider>
);
};