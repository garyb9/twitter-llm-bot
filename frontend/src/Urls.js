import React, { useEffect } from "react";
import {BrowserRouter, Route, Switch, Redirect, useHistory} from "react-router-dom";
import Minter from "./components/Minter";

function Urls(props) {

  return (
    <div>
      <Switch>
        <Route exact path="/minter/">
          {" "}
          {console.log("debug")}
          <Minter {...props} />
        </Route>
        
      </Switch>
    </div>
  );
}

export default Urls;
