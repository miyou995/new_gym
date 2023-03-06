// api.get(`${process.env.REACT_APP_API_URL}/rest-api/clients-name-drop/`).then(res => {
//     console.log(res.status);
//     setUStatus(res.status);
//  }).catch(error => {
//     if (error.response) {
//        console.log(error.response.data);
//        console.log(error.response.status);
//        console.log(error.response.headers);
//        setUStatus(error.response.status);
//     }
//  })


export const SET_CONTRIBUTORS = "SET_CONTRIBUTORS";
export const SET_ERROR = "SET_ERROR";

const dataReducer = (state, action) => {
  // reducer is going to update part of the global state
  // action.type is defining what is to be updated
  // reducer returns the new state

  //  action object
  // {
  // type: SET_CONTRIBUTORS
  // contributors: someValue
  // }

  switch (action.type) {
    case SET_CONTRIBUTORS:
      return {
        // we want to keep a copy of the existing state
        ...state,
        // the elements in the state we want to change
        contributors: action.contributors,
        loading: false,
        error: null
      };
    case SET_ERROR:
      return {
        ...state,
        loading: false,
        contributors: null,
        error: action.error
      };
    default:
      return state;
  }
};

export default dataReducer;
