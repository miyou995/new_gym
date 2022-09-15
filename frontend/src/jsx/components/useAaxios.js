import axios from "axios";
import { useEffect, useRef, useState } from "react";
import useAxios from "./useAxios";



 const useAaxios = (url, method, payload) => {
    const [data, setData] = useState(null);
    const [error, setError] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [transactionStatus, setTransactionStatus] = useState(null);
    const [clientStatus, setClientStatus] = useState(null);
     const [clientsStatus, setClientsStatus] = useState(null);
    const [coachStatus, setCoachStatus] = useState(null);
    const [personnelStatus, setPersonnelStatus] = useState(null);
    const [presenceStatus, setPresenceStatus] = useState(null);
    const [tresorieStatus, setTresorieStatus] = useState(null);
    const [userStatus, setUserStatus] = useState(null);







    
    const api = useAxios();

    // const controllerRef = useRef(new AbortController());
    // const cancel = () => {
    //     controllerRef.current.abort();
    // };

    useEffect(() => {
        (async () => {
            try {
                const response = await api.request({
                    data: payload,
                    method,
                    url,
                })
                setData(response.data);
                setClientStatus(response.status);
                setClientsStatus(response.status);
                setClientsStatus(response.json);
                setTransactionStatus(response.status);
                setCoachStatus(response.status);
                setPersonnelStatus(response.status);
                setPresenceStatus(response.status);
                setTresorieStatus(response.status);
                setUserStatus(response.status);
                console.log('client status', clientStatus);

            } catch (error) {
                setError(error.message);
                console.log(error)
                setClientStatus(error.response.status);
                setClientsStatus(error.response.status);
                setTransactionStatus(error.response.status);
                setCoachStatus(error.response.status);
                setPersonnelStatus(error.response.status);
                setPresenceStatus(error.response.status);
                setTresorieStatus(error.response.status);
                setUserStatus(error.response.status);

            } finally {
                setLoaded(true);
            }
        })();
    }, []);

     return { data, error, loaded, clientStatus, clientsStatus, transactionStatus, coachStatus, personnelStatus, presenceStatus, tresorieStatus, userStatus };

    
    //  useEffect(() => {
    //      api.get(url).then(res => {
    //          setData(res.data);
    //          setStatus(res.status);
    //      }).catch(error => {
    //          if (error.response) {
    //             console.log(error.response.data);
    //             console.log(error.response.status);
    //             console.log(error.response.headers);
    //             setError(error.message);
    //             setStatus(error.response.status);
    //         }
    //      }).finally(() =>
    //          setLoaded(true)
    //      )
    //  }, []);
     

    // return { data,error, loaded , status};

};

export default useAaxios;