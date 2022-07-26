import React, { useReducer} from "react";
// import HandleClient from './HandleClient';
// import AddEditClient from './AddEditClient';

import CreateClient from './ClientCreate'



const initialClients = {
    clients:[ ]
};

export const ClientsContext = React.createContext()


const clientReducer = (clientState, action) => {
    switch(action.type){
        case "get":
            return {...clientState, clients:action.payload}
        case "add":
            const addedClient = [...clientState.clients, action.payload]
            return {...clientState, clients:addedClient}
        case "edit":
            return initialClients
        case "delete":
                return initialClients
        default :
            return initialClients
    }
}

const Clients = () => {
    const [clientState, dispatcher] = useReducer(clientReducer, initialClients)
    return (
        <ClientsContext.Provider value={{clientState, dispatcher}}>
            <CreateClient/>
        </ClientsContext.Provider>
    )} 

export default Clients;