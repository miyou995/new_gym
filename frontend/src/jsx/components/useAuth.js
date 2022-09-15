import { useEffect, useState } from "react";
import useAxios from "./useAxios";


 const useAuth = (url, method) => {
    const [auth, setauth] = useState(null)
    const api = useAxios();
    useEffect(  () => {
       api.request({method,url}).then( res => {
       if (res.status == 200) {
        setauth(true) 
       } else {
          setauth(false) 
       }
     }).catch( err => {
        setauth(false) 
     })
   }, [url])
   return auth
};
export default useAuth;