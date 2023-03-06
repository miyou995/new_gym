import React from "react";
import useAxios from "./components/useAxios";
import { useEffect, useState, useReducer } from "react";
import axios from "axios";
import dataReducer, { SET_CONTRIBUTORS } from "./dataReducer";

const useRequest = url => {
  const [state, dispatch] = useReducer(dataReducer, {
    loading: true,
    contributors: null,
    error: null
  });
  
  // const [contributors, setContributors] = useState(null);
  // const [loading, setLoading] = useState(true);
  // const [error, setError] = useState(null);
  useEffect(() => {
    axios({
      url,
      method: "GET"
    })
      .then(result => {
        // setContributors(result.data);
        // setLoading(false);
        // setError(null);

        dispatch({ type: SET_CONTRIBUTORS, contributors: result.data });
      })
      .catch(err => {
        // setContributors(null);
        // setLoading(false);
        // setError("Error loading data");
        dispatch({ type: SET_ERROR, error: "Error loading data" });
      });
  }, [url]);

  return {
    // contributors,
    // loading,
    // error

    state
  };
};

export default useRequest;
