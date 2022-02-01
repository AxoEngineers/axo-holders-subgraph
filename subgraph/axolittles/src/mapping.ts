import { BigInt } from "@graphprotocol/graph-ts"
import {
  axolittles,
  Approval,
  ApprovalForAll,
  Mint,
  OwnershipTransferred,
  Transfer
} from "../generated/axolittles/axolittles"

let stakeAddressV1 = "0x1ca6e4643062e67ccd555fb4f64bee603340e0ea"
let stakeAddressV2 = "0x1ca6e4643062e67ccd555fb4f64bee603340e0e2"
let nullAddress = "0x0000000000000000000000000000000000000000"

import { AxoHolder, Tran, AxoMint, Axolittle } from "../generated/schema"

export function handleApproval(event: Approval): void {}

export function handleApprovalForAll(event: ApprovalForAll): void {}

export function handleMint(event: Mint): void {
  let minting = new AxoMint(event.transaction.hash.toHex())

  // minting.to = AxoHolder.load(event.params.owner.toHex())
  // if (minting.to == null) {
  //   minting.to = new AxoHolder(event.params.owner.toHex())
  // }

  minting.to = event.params.owner.toHex()
  minting.token_id = event.params.tokenId
  minting.blockHeight = event.block.number
  minting.timestamp = event.block.timestamp
  minting.save()
}

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

  let axo = Axolittle.load(event.params.tokenId.toString())
  if (axo == null) {
    axo = new Axolittle(event.params.tokenId.toString())
    axo.mintBlock = event.block.number
  }
  axo.owner = event.params.to.toHex()

  if (event.params.to.toHex() == stakeAddressV1) {
    //if this is a staking v1 transfer
    axo.stakedOwnerV1 = event.params.from.toHex()
  } else {
    axo.stakedOwnerV1 = nullAddress
  }

  if (event.params.from.toHex() == stakeAddressV1) {
    //if this is an unstaking v1 transfer
    axo.stakedOwnerV1 = nullAddress
  }

  if (event.params.to.toHex() == stakeAddressV2) {
    //if this is a staking v2 transfer
    axo.stakedOwnerV2 = event.params.from.toHex()
  } else {
    axo.stakedOwnerV2 = nullAddress
  }

  if (event.params.from.toHex() == stakeAddressV1) {
    //if this is an unstaking v2 transfer
    axo.stakedOwnerV2 = nullAddress
  }


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
  transfer.token_id = event.params.tokenId
  transfer.blockHeight = event.block.number
  transfer.timestamp = event.block.timestamp
  transfer.transaction_id = event.transaction.hash.toHex()
  fromAccount.save()
  toAccount.save()
  transfer.save()
  axo.save()

}

