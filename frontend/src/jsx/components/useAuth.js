import { useEffect, useState } from "react";
import useAxios from "./useAxios";


 const useAuth = (url, method) => {
   const [auth, setauth] = useState(null)
   const [loading, setLoading] = useState(false);

    const api = useAxios();

   const makeIt = async() => {
      await api.request({method, url}).then( res => {
         if (res.status == 200) {
          setauth(true) 
         } else {
           setauth(false) 
         }
       }).catch( err => {
           setauth(false) 
  
       }).finally(() =>{
         setLoading(true)
        }) 
   }
    useEffect( () => {
      makeIt()
   }, [url])
   return [auth, loading]
};
export default useAuth;