import React, { useReducer} from "react";

import AddSalle from './SalleCreate'


const initialSalleState = {
    salles:[ ]
};


export const SalleContext = React.createContext()

function Salle() {
    const [state, dispatch] = useReducer(salleReducer,initialSalleState)
    return(
        <SalleContext.Provider value={{state,dispatch}} >
            <AddSalle/>
        </SalleContext.Provider>
    )}

function salleReducer(state, action){
    switch(action.type){
        case  "delete":
            const generatedSallesAfterDelete = state.salles.filter( salle => salle.id !== action.payload.id)
            return {...state, salles: generatedSallesAfterDelete}
        
        case "get":
            return {...state, salles:action.payload}
        
        case "add":
            const addedSalles = [...state.salles, action.payload]
            return {...state, salles:addedSalles}
        default: 
            return initialSalleState
    }    
}
export default Salle ;