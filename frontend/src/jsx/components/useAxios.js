import axios from 'axios'

const useAxios = () => {
  const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);

const axiosInstance = axios.create({
    baseURL: `${process.env.REACT_APP_API_URL}`,
    timeout: 5000,
    headers: {
        'Authorization': "JWT " + localStorage.getItem('access_token'),
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});
axiosInstance.interceptors.response.use(
    response => response,
    error => {
      console.log('response', error);
      const originalRequest = error.config;
      
      if (error.response.status === 401 && error.response.statusText === "Unauthorized") {
          const refresh_token = localStorage.getItem('refresh_token');
          const access_token = localStorage.getItem('access_token');
          console.log(refresh_token, 'REFFFFFRESH');
          return axiosInstance
              .post('api/token/refresh/', {refresh: refresh_token})
              .then((response) => {
                  console.log('ressponse for refresh', response);
                  localStorage.setItem('access_token', response.data.access);
                  localStorage.setItem('refresh_token', response.data.refresh);

                  axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                  originalRequest.headers['Authorization'] = "JWT " + response.data.access;

                  return axiosInstance(originalRequest);
              })
              .catch(err => {
                  console.log(err)
              });
      }
      return axiosInstance
  }
);
};
export default useAxios;
