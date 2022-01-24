const path = require("path");
//var HDWalletProvider = require("truffle-hdwallet-provider");
const HDWalletProvider = require("truffle-hdwallet-provider-privkey");
const providerAddress = 'https://ropsten.infura.io/v3/e0612a9ac52d4e0ea8b800c5b24e48fb';
const privKeys = ['YOUR PRIVKEY HERE'];

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "client/src/contracts"),
  networks: {
    develop: {
      host: "127.0.0.1", // Random IP for example purposes (do not use)
      port: 8545,
      network_id: 1,        // Ethereum public network
      from:"0x5824bcb644835f3f31e0aa8d3f5733a609b6cab8"
    },
    live: {
      host: "127.0.0.1", // Random IP for example purposes (do not use)
      port: 8545,
      network_id: 15,        // Ethereum public network
      // optional config values:
      // gas
      // gasPrice
      // from - default address to use for any transaction Truffle makes during migrations
      // provider - web3 provider instance Truffle should use to talk to the Ethereum network.
      //          - function that returns a web3 provider instance (see below.)
      //          - if specified, host and port are ignored.
      // skipDryRun: - true if you don't want to test run the migration locally before the actual migration (default is false)
      // confirmations: - number of confirmations to wait between deployments (default: 0)
      // timeoutBlocks: - if a transaction is not mined, keep waiting for this number of blocks (default is 50)
      // deploymentPollingInterval: - duration between checks for completion of deployment transactions
      // disableConfirmationListener: - true to disable web3's confirmation listener
    },
    ropsten: {
      provider: function() {
        //return new HDWalletProvider(MNEMONIC, providerAddress)
        return new HDWalletProvider(privKeys, providerAddress)
      },
      host: "127.0.0.1", // Random IP for example purposes (do not use)
      port: 8545,
      network_id: 3
    },
    localPrivateNetwork: {
      // provider: function() {
      //   //return new HDWalletProvider(MNEMONIC, "https://ropsten.infura.io/YOUR_API_KEY")
      //   return new HDWalletProvider(MNEMONIC, "https://127.0.0.1:8545")
      // },
      host: "127.0.0.1", // Random IP for example purposes (do not use)
      port: 8545,
      network_id: "*"
    }
  },
  compilers: {
    solc: {
      version: "^0.8.0"
    }
  }
};
