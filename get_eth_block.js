const EthDater = require('ethereum-block-by-date');
const Web3 = require('web3');

const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'));

const dater = new EthDater(
    web3 // Web3 object, required.
);

async function get_block() {

    let block = await dater.getDate(
        '2022-03-03T00:00:00Z', // Date, required. Any valid moment.js value: string, milliseconds, Date() object, moment() object.
        true // Block after, optional. Search for the nearest block before or after the given date. By default true.
    );
    return block;
}

let block = get_block()
block.then(function(result) {
    console.log(result) // "Some User token"
 })