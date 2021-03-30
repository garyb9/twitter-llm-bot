import React from 'react';
import Web3 from "web3";
import axios from "axios";
// import { useHistory, BrowserRouter, Route} from "react-router-dom";
import * as settings from "../settings";
import Box from '@material-ui/core/Box';


export default function CheckWeb3(props) {
  // const history = useHistory();
  const [isWaiting, setIsWaiting] = React.useState(false);
  const [address, setAddress] = React.useState("");

  const handleButtonClick = async (e) => {
    var web3 = new Web3();
    // Modern dapp browsers...
    if (window.ethereum) {
      window.web3 = new Web3(window.ethereum);
      try {
        // Request account access if needed
        setIsWaiting(true);
        await window.ethereum.enable();
        // Acccounts now exposed
        // web3.eth.sendTransaction({/* ... */});
      } 
      catch (error) {
        // User denied account access...
        console.log(error);
      }
      finally {
        setIsWaiting(false);
      }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
      window.web3 = new Web3(web3.currentProvider);
      // Acccounts always exposed
      // web3.eth.sendTransaction({/* ... */});
    }
    window.ethereum.enable();

    if (typeof web3 != "undefined") {
      // console.log(window.web3.currentProvider);
      window.ethereum.enable();
    }
    // else {
    //   this.web3Provider = new Web3.providers.WebsocketProvider(
    //     settings.INFURA_WEBSOCKET_API
    //   );
    //   window.ethereum.enable();
    // }

    var address = window.ethereum.selectedAddress;

    axios.post(`${settings.API_SERVER}/api/app/tokenuri/`, {
          address: address,
        })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
    });
    
    setAddress(address);
  };

  return (
    <div className="Web3Utils">
      <header className="Web3-header">

        <button disabled={isWaiting} onClick={handleButtonClick}>
          Connect Metamask
        </button> 
        
        <Box bgcolor={address? "success.main" : "primary.main"} color="primary.contrastText" p={2}>
          Metamask Address: {address}
        </Box>

      </header>
    </div>
  );
}
