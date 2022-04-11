import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
// import productData from "../productData";
import axios from "axios";
import { Tab, Button } from "react-bootstrap";
import { useGetAPI } from "../useAPI";

import product1 from "../../../images/product/1.jpg";

const PersonnelDetail = (props) => {
  const [personnel, setPersonnel] = useState({});

  const id = props.match.params.id;

  let PersonnelDetailEndpoint = `${process.env.REACT_APP_API_URL}/rest-api/personnel/${id}`;
  const personnelData = useGetAPI(PersonnelDetailEndpoint);
  useEffect(() => {
    const personnelSelected = personnelData;
    setPersonnel(personnelSelected);
  }, [personnelData]);

  const capitalizeFirstLetter = (word) => {
    if (word) return word.charAt(0).toUpperCase() + word.slice(1);
    return "";
  };

  return (
    <>
      <div className="page-titles">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/ecom-product-detail">Layout</Link>
          </li>
          <li className="breadcrumb-item active">
            <Link to="/ecom-product-detail">Blank</Link>
          </li>
        </ol>
      </div>
      <div className="row">
        <div className="col-lg-12">
          <div className="card">
            <div className="card-body">
              <div className="row">
                <div className="col-xl-3 col-lg-6  col-md-6 col-xxl-5 ">
                  {/* Tab panes */}
                  <Tab.Container defaultActiveKey="first">
                    <Tab.Content>
                      <Tab.Pane eventKey="first">
                        <img className="img-fluid" src={product1} alt="image" />
                      </Tab.Pane>
                    </Tab.Content>
                  </Tab.Container>
                </div>
                {/*Tab slider End*/}
                <div className="col-xl-9 col-lg-6  col-md-6 col-xxl-7 col-sm-12">
                  <div className="product-detail-content">
                    {/*Product details*/}
                    <div className="new-arrival-content pr">
                      <p
                        className="price"
                        style={{ textTransform: "capitalize" }}
                      >
                        {personnel.last_name} {personnel.first_name}{" "}
                        {personnel.id}
                      </p>
                      <h6>
                        Type d'abonnement: <span className="item"></span>{" "}
                      </h6>
                      <h6>
                        Civilité:{" "}
                        <span className="item">
                          {personnel.civility_display}
                        </span>{" "}
                      </h6>
                      <h6>
                        Téléphone:{" "}
                        <span className="item">
                          <a href={`tel:${personnel.phone}`}>
                            {" "}
                            {personnel.phone}
                          </a>
                        </span>
                      </h6>
                      <h6>
                        email:{" "}
                        <span className="item">
                          <a href={`mailto:${personnel.email}`}>
                            {" "}
                            {personnel.email}
                          </a>
                        </span>
                      </h6>
                      <h6>
                        Groupe sanguin:&nbsp;&nbsp;{" "}
                        <span className="badge badge-success light">
                          {personnel.blood}
                        </span>{" "}
                      </h6>
                      <h6>
                        Adresse:{" "}
                        <span className="item">{personnel.adress}</span>{" "}
                      </h6>
                      <h6>
                        Nationalité:{" "}
                        <span className="item">{personnel.nationality}</span>{" "}
                      </h6>
                      <h6>
                        Date de naissance:{" "}
                        <span className="item">{personnel.birth_date}</span>{" "}
                      </h6>
                      <h6>
                        Etat:{" "}
                        <span className="item">{personnel.state_display}</span>{" "}
                      </h6>
                      <h6>
                        Note: <span className="item">{personnel.note}</span>{" "}
                      </h6>
                      <h6>
                        Date d'adhesion:{" "}
                        <span className="item">{personnel.date_added}</span>{" "}
                      </h6>

                      <div className="shopping-cart mt-3">
                        <Link
                          to={`/personnel/edit/${personnel.id}`}
                          className="btn btn-primary ml-auto"
                        >
                          Modifier
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default PersonnelDetail;
