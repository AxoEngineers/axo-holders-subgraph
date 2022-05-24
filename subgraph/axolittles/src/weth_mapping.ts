import { BigInt } from "@graphprotocol/graph-ts"
import {
  Transfer
} from "../generated/wrapped_eth/wrapped_eth"

import { TransferTransaction } from "../generated/schema"

export function handleWethTransfer(event: Transfer): void {
  let transaction = TransferTransaction.load(event.transaction.hash.toHex())
  if (transaction == null) {
    // need to create instance
    transaction = new TransferTransaction(event.transaction.hash.toHex())
    transaction.nTransfers = 0
    transaction.blockHeight = event.block.number
    transaction.timestamp = event.block.timestamp
    transaction.valueWei = event.transaction.value
    transaction.valueWrappedWei = new BigInt(0)
  }
  transaction.valueWrappedWei = transaction.valueWrappedWei.plus(event.params.wad)
  transaction.valueBothWei = transaction.valueWei.plus(transaction.valueWrappedWei)
  transaction.save()
}