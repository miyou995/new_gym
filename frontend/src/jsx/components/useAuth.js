import { useEffect, useState } from "react";
import useAxios from "./useAxios";


 const useAuth = (url, method, payload) => {
    const [auth, setauth] = useState(null)
    const [data, setData] = useState(null)

    const api = useAxios();
    useEffect(  () => {
       api.request({ data: payload, method,url}).then( res => {
       if (res.status == 200) {
        setData(res.data)
        setauth(true) 
       } else {
         setauth(false) 
       }
     }).catch( err => {
         console.log(err.response.status)
         setauth(false) 
     })
   }, [url])

   return auth
};
export default useAuth;