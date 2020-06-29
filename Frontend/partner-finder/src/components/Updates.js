import React from "react";
import { Button } from "@material-ui/core";
import { Msgtoshow } from "./Msgtoshow";
import { BACKEND_URL } from "../utils";

function Updates(props) {
  const [state, setState] = React.useState({
    EU: "",
    B2MATCH: "",
    firstLoading: true,
  });

  const [msgState, setMsgState] = React.useState({
    title: "",
    body: "",
    visible: false,
  });

  if (state.firstLoading) {
    setState({ ...props.state });
  }

  /**
   * Method that upadtes the B2MATCH events in our DB (getting the future events) and
    returns the last update date from the backend and show it in the GUI
   */
  const updateB2match = () => {
    let url = new URL(BACKEND_URL + "events/update_upcoming_events/");
    fetch(url, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("error" in resp) {
          setMsgState({
            title: "Failed",
            body: "Error while updating the events",
            visible: true,
          });
        } else {
          setMsgState({
            title: "Success",
            body: "B2match has been updated successfully",
            visible: true,
          });
        }
      })
      .catch((error) =>
        setMsgState({
          title: "Failed",
          body: "Error while updating B2match data",
          visible: true,
        })
      );
  };

  /**
   * Method that upadtes the EU Organizations in our DB and
    returns the last update date from the backend and show it in the GUI
   */
  const updateEU = () => {
    let url = new URL(BACKEND_URL + "organizations/update_organizations/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("error" in resp) {
          setMsgState({
            title: "Failed",
            body: "Error while updating the EU data.",
            visible: true,
          });
        } else {
          setMsgState({
            title: "Success",
            body: "EU has been updated successfully.",
            visible: true,
          });
        }
      })
      .catch((error) =>
        setMsgState({
          title: "Failed",
          body: "Error while updating EU data.",
          visible: true,
        })
      );
  };

  return (
    <React.Fragment>
      <Msgtoshow
        {...msgState}
        handleClose={() => setMsgState({ ...msgState, visible: false })}
      />
      <div>
        <h1>Updates</h1>
      </div>
      <div style={{ "margin-top": "30px" }}>
        <h1 style={{ "margin-left": "30px" }}>B2MATCH</h1>
      </div>
      <div className="update">
        <h2 id="textFontFamily" style={{ "margin-left": "50px" }}>
          Last Update
        </h2>
        <h3 style={{ marginTop: "8%", fontSize: "15px" }}>{state.B2MATCH}</h3>
      </div>
      <div style={{ "margin-left": "50px", "margin-top": "50px" }}>
        <Button
          color="primary"
          round
          variant="contained"
          id="BackgroundColor"
          onClick={updateB2match}
          style={{ width: "20%" }}
        >
          Update Now
        </Button>
      </div>
      <div style={{ "margin-top": "30px" }}>
        <h1 style={{ "margin-left": "30px" }}>EU</h1>
      </div>
      <div className="update">
        <h2 id="textFontFamily" style={{ "margin-left": "50px" }}>
          Last Update
        </h2>
        <h3 style={{ marginTop: "8.5%", fontSize: "15px" }}>{state.EU}</h3>
      </div>
      <div style={{ "margin-left": "50px", "margin-top": "50px" }}>
        <Button
          color="primary"
          round
          variant="contained"
          id="BackgroundColor"
          onClick={updateEU}
          style={{ width: "20%" }}
        >
          Update Now
        </Button>
      </div>
      <div style={{ "margin-top": "10%" }}>
        <h2
          style={{
            textAlign: "center",
            "font-weight": "500",
          }}
        >
          ** There is an automatically updates every month for both EU & B2MATCH
          **
        </h2>
      </div>
    </React.Fragment>
  );
}
export default Updates;
