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
  }
  transaction.valueWrappedWei = event.params.wad
  transaction.save()
}