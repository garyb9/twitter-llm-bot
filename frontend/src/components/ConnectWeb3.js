import React from 'react';
import { Web3, Web3Provider } from 'web3';
import { Web3ReactProvider, createWeb3ReactRoot } from '@web3-react/core'
import { InjectedConnector } from '@web3-react/injected-connector'

function getLibrary(provider) {
  return new Web3Provider(provider) // this will vary according to whether you use e.g. ethers or web3.js
}


export default function ConnectWeb3 () {
    // const Web3ReactProviderReloaded = createWeb3ReactRoot('anotherOne')
    const injected = new InjectedConnector({ 
        supportedChainIds: [
            1, // Mainnet
            3, // Ropsten
            4, // Rinkeby
            5, // Goerli
            42 // Kovan
        ] 
    })

  return (
    <Web3ReactProvider getLibrary={getLibrary}>
      {console.log(injected)}
    </Web3ReactProvider>
  )
}