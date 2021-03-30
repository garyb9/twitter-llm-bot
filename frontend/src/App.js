import logo from './logo.svg';
import ConnectWeb3 from './components/ConnectWeb3'
import CheckWeb3 from "./components/Web3Utils";
import './App.css';

function App(props) {
  return (
    <div className="App">
      <header className="App-header">
          {/* <ConnectWeb3/> */}
           
        <img src={logo} className="App-logo" alt="logo" />

        <button onClick={() => CheckWeb3()}>Connect Metamask</button> 

      </header>
    </div>
  );
}

export default App;
