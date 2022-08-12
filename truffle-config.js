const path = require("path");
//var HDWalletProvider = require("truffle-hdwallet-provider");
const HDWalletProvider = require("truffle-hdwallet-provider-privkey");
//const providerAddress = 'https://ropsten.infura.io/v3/e0612a9ac52d4e0ea8b800c5b24e48fb';
//const privKeys = ['YOUR PRIVKEY HERE'];

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "client/src/contracts"),
  networks: {
    localPrivateNetwork: {
      // provider: function() {
      //   //return new HDWalletProvider(MNEMONIC, "https://ropsten.infura.io/YOUR_API_KEY")
      //   return new HDWalletProvider(MNEMONIC, "https://127.0.0.1:8545")
      // },
      host: "127.0.0.1", // Random IP for example purposes (do not use)
      port: 7545,
      network_id: "*"
    }
  },
  compilers: {
    solc: {
      version: "^0.8.0"
    }
  }
};
