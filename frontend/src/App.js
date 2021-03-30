import logo from './logo.svg';
// import Urls from "./Urls";
import CheckWeb3 from "./components/Web3Utils";
import Minter from "./components/Minter";
import './App.css';

function App(props) {
  return (
    <div className="App">
      <header className="App-header">
           
        <img src={logo} className="App-logo" alt="logo" />

        <CheckWeb3 {...props}>
          {/* <Urls {...props} /> */}
        </CheckWeb3>

        <Minter {...props} />

      </header>
    </div>
  );
}

export default App;
