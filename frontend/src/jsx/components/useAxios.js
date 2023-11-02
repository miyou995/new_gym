import axios from "axios";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";


const baseURL = `${process.env.REACT_APP_API_URL}`;

const useAxios = () => {
    const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);
    
  const axiosInstance = axios.create({
    baseURL,
    headers: { Authorization: `JWT ${authTokens?.access}` }
  });
  axiosInstance.interceptors.request.use(async request => {
    const user = jwt_decode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
    if (!isExpired) return request;
    const response = await axios.post(`${baseURL}/rest-api/auth/token/refresh/`, {
      refresh: authTokens.refresh
    }).catch(err => {
      if (err.request.status === 401) {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem("authTokens");
        window.location ="/login";
      }
    })
    localStorage.setItem('authTokens', JSON.stringify(response.data))
    setAuthTokens(response.data)
    setUser(jwt_decode(response.data.access))
    request.headers.Authorization = `JWT ${response.data.access}`
    return request
  })
  return axiosInstance;
};
export default useAxios;
