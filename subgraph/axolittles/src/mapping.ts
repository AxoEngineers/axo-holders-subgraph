import { BigInt } from "@graphprotocol/graph-ts"
import {
  axolittles,
  // Approval,
  // OwnershipTransferred,
  Mint,
  Transfer,
  // Approval,
  // ApprovalForAll
} from "../generated/axolittles/axolittles"
import { AxoHolder, Tran, AxoMint } from "../generated/schema"

export function handleMinting(event: Mint): void {
  let minting = new AxoMint(event.transaction.hash.toHex())

  // minting.to = AxoHolder.load(event.params.owner.toHex())
  // if (minting.to == null) {
  //   minting.to = new AxoHolder(event.params.owner.toHex())
  // }

  minting.to = event.params.owner.toHex()
  minting.axo_id = event.params.tokenId
  minting.blockHeight = event.block.number
  minting.timestamp = event.block.timestamp
  minting.save()
}

export function handleTransfer(event: Transfer): void {
  // Entities can be loaded from the store using a string ID; this ID
  // needs to be unique across all entities of the same type
  let fromAccount = AxoHolder.load(event.params.from.toHex())
  if (fromAccount == null) {
    fromAccount = new AxoHolder(event.params.from.toHex())
  }

  let toAccount = AxoHolder.load(event.params.to.toHex())
  if (toAccount == null) {
    toAccount = new AxoHolder(event.params.to.toHex())
  }

  let transfer = new Tran(event.transaction.hash.toHex())
  transfer.from = event.params.from.toHex()
  transfer.to = event.params.to.toHex()
  transfer.token_id = event.params.tokenId
  transfer.blockHeight = event.block.number
  transfer.timestamp = event.block.timestamp
  fromAccount.save()
  toAccount.save()
  transfer.save()

}
