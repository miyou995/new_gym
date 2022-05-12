
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
    timeout: 5000,
    headers: { Authorization: `JWT ${authTokens?.access}` }
  });

  axiosInstance.interceptors.request.use(async req => {
    const user = jwt_decode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (!isExpired) return req;

    const response = await axios.post(`${baseURL}/api/token/refresh/`, {
      refresh: authTokens.refresh
    });

    localStorage.setItem("authTokens", JSON.stringify(response.data));

    setAuthTokens(response.data);
    setUser(jwt_decode(response.data.access));

    req.headers.Authorization = `JWT ${response.data.access}`;
    return req;
  });

  return axiosInstance;
};

export default useAxios;