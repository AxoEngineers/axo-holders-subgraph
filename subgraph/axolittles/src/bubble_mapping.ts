import { BigInt } from "@graphprotocol/graph-ts"
import {
  Transfer
} from "../generated/bubble/bubble"

// let stakeAddressV1 = "0x1ca6e4643062e67ccd555fb4f64bee603340e0ea"
// let stakeAddressV2 = "0xfa822d611e583a6fb879c03645ddfd1c8877252a"
let nullAddress = "0x0000000000000000000000000000000000000000"

import { AxoHolder, ClaimBubble } from "../generated/schema"

export function handleBubbleTransfer(event: Transfer): void {
    // make sure this is a claim/mint
    if (event.params.from.toHex() == nullAddress) {
        let toAccount = AxoHolder.load(event.params.to.toHex())
        if (toAccount == null) {
            toAccount = new AxoHolder(event.params.to.toHex())
            toAccount.firstActiveBlock = event.block.number
        }
        let txnString = event.transaction.hash.toHexString()
        let fromString = event.params.from.toHexString()
        let toString = event.params.to.toHexString()
        let claim_id = txnString+fromString+toString
        let claim = new ClaimBubble(claim_id)
        claim.to = event.params.to.toHex()
        claim.amount = event.params.value
        claim.blockHeight = event.block.number
        claim.timestamp = event.block.timestamp
        claim.transaction_id = event.transaction.hash.toHex()
        claim.save()
        toAccount.save()
    }
  }