import useAxios from "../useAxios";


const url = api.create({
    baseURL: `${process.env.REACT_APP_API_URL}/rest-api`,
});


export const getCiv = (body) => {
    let result = url
        .get('/clients')
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
        });

    return result;
};