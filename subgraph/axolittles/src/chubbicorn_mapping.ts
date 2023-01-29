import { BigInt } from "@graphprotocol/graph-ts"
import {
  chubbicorns,
  Approval,
  ApprovalForAll,
  OwnershipTransferred,
  Transfer,
  ChubbicornMigrated
} from "../generated/chubbicorns/chubbicorns"

let nullAddress = "0x0000000000000000000000000000000000000000"

import { AxoHolder, Tran, TransferTransaction, Chubbicorn } from "../generated/schema"

export function handleApproval(event: Approval): void {}

export function handleApprovalForAll(event: ApprovalForAll): void {}

export function handleMint(event: ChubbicornMigrated): void {}

export function handleOwnershipTransferred(event: OwnershipTransferred): void {}

export function handleTransfer(event: Transfer): void {
  // Entities can be loaded from the store using a string ID; this ID
  // needs to be unique across all entities of the same type
  let fromAccount = AxoHolder.load(event.params.from.toHex())
  if (fromAccount == null) {
    fromAccount = new AxoHolder(event.params.from.toHex())
    fromAccount.firstActiveBlock = event.block.number
  }

  let toAccount = AxoHolder.load(event.params.to.toHex())
  if (toAccount == null) {
    toAccount = new AxoHolder(event.params.to.toHex())
    toAccount.firstActiveBlock = event.block.number
  }

  let corn = Chubbicorn.load(event.params.tokenId.toString())
  if (corn == null) {
    corn = new Chubbicorn(event.params.tokenId.toString())
    corn.mintBlock = event.block.number
  }
  corn.owner = event.params.to.toHex()

  fromAccount.lastActiveBlock = event.block.number
  toAccount.lastActiveBlock = event.block.number
  
  let txnString = event.transaction.hash.toHexString()
  let tokenString = event.params.tokenId.toString()
  let fromString = event.params.from.toHexString()
  let toString = event.params.to.toHexString()
  //this complex id is needed because
  //some transactions include multiple transfers of the same
  //token, for example nftx.io staking
  let transfer_id = txnString + tokenString + fromString + toString
  let transfer = new Tran(transfer_id)
  transfer.from = event.params.from.toHex()
  transfer.to = event.params.to.toHex()
  transfer.token_type = 'chubbicorn'
  transfer.token_id = event.params.tokenId
  transfer.blockHeight = event.block.number
  transfer.timestamp = event.block.timestamp

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
  transaction.valueWei = event.transaction.value
  transaction.valueBothWei = transaction.valueWei.plus(transaction.valueWrappedWei)
  // incriment for each axo transfered.
  transaction.nTransfers += 1
  
  transfer.transaction = event.transaction.hash.toHex()
  // transfer.value = event.transaction.value.plus(transaction.valueWrappedWei)
  fromAccount.save()
  toAccount.save()
  transfer.save()
  corn.save()
  transaction.save()
}
