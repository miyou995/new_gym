import { Route} from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";


const PrivateRoute = ({ children, ...rest }) => {
  let { user } = useContext(AuthContext);
  
  const redirectToLogin = () => {
    window.location ="/login" 
  }
  return <Route {...rest}>{!user ? redirectToLogin : children}</Route>;
};
export default PrivateRoute;




