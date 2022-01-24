import { BigInt } from "@graphprotocol/graph-ts"
import {
  Axolittles,
  Approval,
  ApprovalForAll,
  Mint,
  OwnershipTransferred,
  Transfer
} from "../generated/Axolittles/Axolittles"
import { AxoHolder, Tran, AxoMint } from "../generated/schema"

export function handleApproval(event: Approval): void {}
  // // Entities can be loaded from the store using a string ID; this ID
  // // needs to be unique across all entities of the same type
  // let entity = ExampleEntity.load(event.transaction.from.toHex())

  // // Entities only exist after they have been saved to the store;
  // // `null` checks allow to create entities on demand
  // if (!entity) {
  //   entity = new ExampleEntity(event.transaction.from.toHex())

  //   // Entity fields can be set using simple assignments
  //   entity.count = BigInt.fromI32(0)
  // }

  // // BigInt and BigDecimal math are supported
  // entity.count = entity.count + BigInt.fromI32(1)

  // // Entity fields can be set based on event parameters
  // entity.owner = event.params.owner
  // entity.approved = event.params.approved

  // // Entities can be written to the store with `.save()`
  // entity.save()

  // Note: If a handler doesn't require existing field values, it is faster
  // _not_ to load the entity from the store. Instead, create it fresh with
  // `new Entity(...)`, set the fields that should be updated and save the
  // entity back to the store. Fields that were not set or unset remain
  // unchanged, allowing for partial updates to be applied.

  // It is also possible to access smart contracts from mappings. For
  // example, the contract that has emitted the event can be connected to
  // with:
  //
  // let contract = Contract.bind(event.address)
  //
  // The following functions can then be called on this contract to access
  // state variables and other data:
  //
  // - contract._baseTokenURI(...)
  // - contract.balanceOf(...)
  // - contract.getApproved(...)
  // - contract.isApprovedForAll(...)
  // - contract.isOpen(...)
  // - contract.maxItems(...)
  // - contract.maxItemsPerTx(...)
  // - contract.mintPrice(...)
  // - contract.name(...)
  // - contract.owner(...)
  // - contract.ownerOf(...)
  // - contract.publicMintPaused(...)
  // - contract.startTimestamp(...)
  // - contract.supportsInterface(...)
  // - contract.symbol(...)
  // - contract.tokenURI(...)
  // - contract.totalSupply(...)
//}

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
  }

  let toAccount = AxoHolder.load(event.params.to.toHex())
  if (toAccount == null) {
    toAccount = new AxoHolder(event.params.to.toHex())
  }
  
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

}

