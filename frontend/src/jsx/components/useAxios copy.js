import { useContext } from "react";
import axios from "axios";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import AuthContext from "../context/AuthContext";

let baseURL = `${process.env.REACT_APP_API_URL}`
console.log('base URL=---------------------------+++++++++++++++++++++>>>>>>>>>>>>>>', baseURL);
const useAxios = () => {
  const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);

  const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,

    headers: {
      'Authorization': "JWT " + localStorage.getItem('access_token'),
      'Content-Type': 'application/json',
      'accept': 'application/json'
  }
  });

  axiosInstance.interceptors.request.use(async req => {
    const user = jwt_decode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
    console.log('axioooooooos');
    if (!isExpired) return req;
    console.log('header access expired');

    const response = await axios.post(`${baseURL}/api/token/refresh/`, {
      refresh: authTokens.refresh
    });
    console.log('response ', response);

    localStorage.setItem("authTokens", JSON.stringify(response.data));

    setAuthTokens(response.data);
    setUser(jwt_decode(response.data.access));

    req.headers.Authorization = `JWT ${response.data.access}`;
    return req;
    console.log('finishshsh');
  });


  return axiosInstance;
};

export default useAxios;