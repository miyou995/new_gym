import { useEffect, useState } from "react";
import useAxios from "./useAxios";


 const useAuth = (url, method) => {
    const [auth, setauth] = useState(null)
   const [loading, setLoading] = useState(false);

    const api = useAxios();
    useEffect(  async () => {
      await api.request({method, url}).then( res => {
       if (res.status == 200) {
        setauth(true) 
       } else {
         setauth(false) 
       }
      console.log(loading)
     }).catch( err => {
         console.log(err.response.status)
         setauth(false) 
        console.log(loading)

     }).finally(() =>{
       setLoading(true)
      }) 
      
   }, [url])

   return [auth, loading]

};

export default useAuth;