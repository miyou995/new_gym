import { useState, useEffect } from "react";
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
const config = { headers: { "Content-Type": "multipart/form-data" } };

export const useGetAPI = (endpoint) => {
  const [data, setDdata] = useState([]);
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    const response = await axios.get(endpoint);
    setDdata(response.data);
  };
  return data;
};

export const usePostAPI = async (endpoint, postData) => {
  await axios.post(endpoint, postData);
};

export const usePutAPI = async (endpoint, newData) => {
  await axios.put(endpoint, newData);
};

export const useDeleteAPI = async (endpoint, newData) => {
  await axios.delete(endpoint);
};
