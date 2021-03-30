
let API_SERVER_VAL = '';

let INFURA_WEBSOCKET = 'wss://mainnet.infura.io/ws/v3/';

switch (process.env.NODE_ENV) {
    case 'development':
        API_SERVER_VAL = 'http://localhost:8000';
        INFURA_WEBSOCKET.concat(process.env.REACT_APP_INFURA_API_KEY);
        break;
    case 'production':
        API_SERVER_VAL = process.env.REACT_APP_API_SERVER;
        break;
    default:
        API_SERVER_VAL = 'http://localhost:8000';
        INFURA_WEBSOCKET.concat(process.env.REACT_APP_INFURA_API_KEY);
        break;
}

export const API_SERVER = API_SERVER_VAL;

export const INFURA_WEBSOCKET_API = INFURA_WEBSOCKET;

export const SESSION_DURATION = 5*3600*1000;