//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MemeContract.sol";

contract Factory is MemeContract{

    MemeContract[] public memeContractsArray;

    function createMemeContract() public {
        MemeContract memeContract = new MemeContract();
        memeContractsArray.push(memeContract);
    }


}
